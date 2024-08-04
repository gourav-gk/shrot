# Shrote Project

## Overview

Shrote is a set of functionalities designed to assist visually challenged individuals. It serves as a prototype code that, when embedded in an eyewear device, can significantly enhance the user's ability to interact with their environment. This project includes features such as audio transcription using Google Speech-to-Text, weather information using RapidAPI, SMS notifications with Twilio, and face recognition. Additionally, Shrote connects to a Google Cloud MySQL database using cloud-sql-proxy.

The ultimate goal of Shrote is to provide a closer-to-eye solution for visually challenged persons, making everyday tasks more accessible and manageable.

## Table of Contents

1. [Setup](#setup)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
2. [Configuration](#configuration)
   - [Google Cloud Service Account](#google-cloud-service-account)
   - [RapidAPI for Weather](#rapidapi-for-weather)
   - [Twilio API Credentials](#twilio-api-credentials)
   - [Face Recognition](#face-recognition)
   - [Google Cloud MySQL](#google-cloud-mysql)
3. [Running the Project](#running-the-project)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)

## Setup

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or later
- Django 3.0 or later
- Google Cloud SDK
- `cloud-sql-proxy` binary
- RapidAPI account
- Twilio account
- OpenCV and `face_recognition` library

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/shrote.git
    cd shrote
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate   # On Windows use `env\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

### Google Cloud Service Account

1. Create a Google Cloud Service Account and download the JSON key file. Name it `key.json` and place it in the root directory of the project.

2. Set up the Google Cloud Speech-to-Text API by following [Google's documentation](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries).

### RapidAPI for Weather

1. Sign up at [RapidAPI](https://rapidapi.com/).

2. Subscribe to the [Weather API](https://weatherapi-com.p.rapidapi.com).

3. Create an `.env` file in the root directory and add your API key:
    ```env
    RAPIDAPI_WEATHER_KEY="your_rapidapi_key"
    ```

### Twilio API Credentials

1. Sign up at [Twilio](https://www.twilio.com/).

2. Create a new project and get your `account_sid` and `auth_token`.

3. In `shrote_app/sms.py`, add your Twilio credentials:
    ```python
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    ```

### Face Recognition

1. Add your facial encoding in `shrote_app/face.py`:
    ```python
    import face_recognition

    # Load a sample picture and learn how to recognize it.
    your_image = face_recognition.load_image_file("path_to_your_image")
    your_face_encoding = face_recognition.face_encodings(your_image)[0]

    # Add more known face encodings and their names
    known_face_encodings = [
        your_face_encoding,
    ]
    known_face_names = [
        "Your Name",
    ]
    ```

### Google Cloud MySQL

1. Create a Google Cloud MySQL database instance by following [Google's documentation](https://cloud.google.com/sql/docs/mysql/create-instance).

2. Download the `cloud-sql-proxy` binary and place it in your project directory.

3. Connect to the MySQL instance using `cloud-sql-proxy`:
    ```bash
    ./cloud-sql-proxy your-instance-connection-name
    ```

4. Update your Django `settings.py` to connect to the MySQL database:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
        }
    }
    ```

## Running the Project

1. Run the migrations:
    ```bash
    python manage.py migrate
    ```

2. Start the development server:
    ```bash
    python manage.py runserver
    ```

## Contributing

1. Fork the repository.

2. Create a new branch:
    ```bash
    git checkout -b feature/your-feature-name
    ```

3. Make your changes and commit them:
    ```bash
    git commit -m 'Add some feature'
    ```

4. Push to the branch:
    ```bash
    git push origin feature/your-feature-name
    ```

5. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
