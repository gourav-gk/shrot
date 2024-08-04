import os
import re
import logging
import requests
import numpy as np
from datetime import datetime
from django.shortcuts import render, redirect
from google.cloud import speech, texttospeech, translate_v2 as translate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from .models import Conversation
from django.conf import settings
from . import sms
from . import object_model as oj
# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Set up the clients
speech_client = speech.SpeechClient.from_service_account_file('key.json')
tts_client = texttospeech.TextToSpeechClient.from_service_account_file('key.json')
translate_client = translate.Client.from_service_account_json('key.json')



def synthesize_speech(text, output_filename="output.mp3", language_code="en-US"):
    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = tts_client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    static_dir = os.path.join(settings.BASE_DIR, 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Save the audio file to the static location
    audio_path = os.path.join(static_dir, 'output.mp3')

    with open(audio_path, "wb") as out:
        out.write(response.audio_content)

    return audio_path



def translate_text(text, target_language="en"):
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

def clean_response(text):
    # Remove special characters and unwanted symbols
    return re.sub(r'[^A-Za-z0-9\s,]', '', text)


def get_current_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_weather(city):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q": city}
    headers = {
        "X-RapidAPI-Key": "",
        "X-RapidAPI-Host": ""
    }
    response = requests.get(url, headers=headers, params=querystring)
    try:
        data = response.json()
        logging.debug(f"Weather API response: {data}")
        if 'current' in data:
            return f"The weather condition in {city} is {data['current']['condition']['text']} and temperature is {data['current']['temp_c']} degree Celsius."
        else:
            return "Sorry, I couldn't retrieve the weather information at the moment."
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        return "An error occurred while fetching the weather information."


def handle_special_queries(query):
    if "time" in query.lower():
        return get_current_time()
    elif "weather" in query.lower():
        parts = query.split("weather in")
        if len(parts) > 1:
            city = parts[1].strip()
            return get_weather(city)
        return "Please specify the city for the weather information."
    elif "help" in query.lower():
        sms.send()
        return "Help request is been sent, please be safe until someone reaches for help"
    elif "front" in query.lower():
        return oj.detect()
    else:
        return None



def index(request):
    conversations = Conversation.objects.all()
    return render(request, 'shrote_app/index.html', {'conversations': conversations})


def start_conversation(request):
    response_text = ""
    lang = "en"
    output_filename = 'static/output.mp3'
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        detected_language = request.POST.get('lang')

        if request.FILES:
            image = request.FILES.get('image')
            if image:
                # Save the uploaded image
                image_path = os.path.join(settings.BASE_DIR, 'static', 'detected_frame.jpg')
                with open(image_path, 'wb') as img:
                    for chunk in image.chunks():
                        img.write(chunk)

        if detected_language != "en":
            user_input = translate_text(user_input, target_language="en")

        print(user_input)

        special_response = handle_special_queries(user_input)
        if special_response:
            response_text = special_response
        else:
            os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
            prompt_template = PromptTemplate(input_variables=["chat_history", "user_input"],
                                             template=("Your name is shrote an AI assistant for the visual impared person you have the answer the question accordingly. Here's the recent conversation:\n"
                                                       "{chat_history}\n"
                                                       "Now, respond to the user's question succinctly: {user_input}"))
            chat_chain = prompt_template | llm
            chat_history = [f"User: {conv.user_input}\nAI: {conv.response_text}" for conv in
                            Conversation.objects.all()]
            formatted_history = "\n".join(chat_history)
            response = chat_chain.invoke({"chat_history": formatted_history, "user_input": user_input})
            response_text = clean_response(response.content)

        Conversation.objects.create(user_input=user_input, response_text=response_text)

        if detected_language != "en":
            response_text = translate_text(response_text, target_language=detected_language)

        print(response_text)

        output_filename = synthesize_speech(response_text, language_code=detected_language)



        #return redirect('index')
    return render(request, 'shrote_app/conversation.html',{'message': response_text, 'lang': lang, 'audio_path': output_filename})

def delete_conversation(request, conversation_id):
    try:
        Conversation.objects.filter(id=conversation_id).delete()
        return redirect('index')  # Redirect to the index page or any other page
    except Conversation.DoesNotExist:
        return render(request, 'shrote_app/error.html', {'message': 'Conversation not found'})