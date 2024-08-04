import cv2
from ultralytics import YOLO
from .face import recognize
import os
from django.conf import settings

# Load the YOLOv8 model
model = YOLO("yolov8n.pt")




def detect():
    # cap = cv2.VideoCapture(video_path)

    cap = cv2.VideoCapture(0)

    # Flag to indicate whether to capture a single frame
    capture_frame = False

    response = ""
    person =""
    object_counts = {}

    frame = cv2.imread('static/detected_frame.jpg')

    if frame is not None:
        if not capture_frame:
            # Run YOLOv8 inference on the frame
            results = model(frame)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            if results[0].boxes:
                for result in results[0].boxes:
                    obj = results[0].names[result.cls[0].item()]

                    if obj in object_counts:
                        object_counts[obj] += 1
                    else:
                        object_counts[obj] = 1

                for obj, count in object_counts.items():
                    response = response+str(count)+" "+obj+", "

                static_dir = os.path.join(settings.BASE_DIR, 'static')
                if not os.path.exists(static_dir):
                    os.makedirs(static_dir)
                img_path = os.path.join(static_dir, 'detected_frame.jpg')

                print(img_path)

                cv2.imwrite(img_path, frame)
                capture_frame = True

                cap.release()
                cv2.destroyAllWindows()

                if "person" in response:
                    faces = recognize()

                    for face in faces:
                        person = person + face + ", "

                    if len(faces) > 0:
                        person = " Which includes "+person[0:-2]


                response = response[0:-2]+" detected."+person

                return response


