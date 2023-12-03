import time
import cv2
import boto3
import numpy
from threading import Thread
VIDEO_URL = "udp://0.0.0.0:11111"

rekognition = boto3.client('rekognition', region_name='us-east-1')

# Capture video frames from tello drone, detect labels and show them
# First connect to the Tello drone Wifi and 
# then send "command" and "streamon"

# Only requirements are opencv-python and boto3 install with:
# pip install opencv-python boto3

def detect_labels(frame):
    image_encoded = cv2.imencode('.jpg', frame)[1]
    image_bytes = (numpy.array(image_encoded)).tobytes()
    response = rekognition.detect_labels(
        Image={'Bytes': image_bytes},
        MinConfidence=77.5
    )
    print()
    for label in response['Labels']:
        print(label['Name'], end =" ")
        # print("Label: " + label['Name'])
        # print("Confidence: " + str(label['Confidence']))
        # print("Instances:")

        # for instance in label['Instances']:
        #     bbox = instance['BoundingBox']
        #     top = bbox['Top']
        #     left = bbox['Left']
        #     width = bbox['Width']
        #     height = bbox['Height']

        #     print(f" Bounding box T: {top}, L: {left}, W: {width}, H: {height}")
        #     print(f" Confidence: {instance['Confidence']} \n")

    return frame

def process_frame(frame):
    epoch = int(time.time())
    if (epoch % 2) == 0:
        #return detect_labels(frame)
        Thread(target=detect_labels, args=(frame,), daemon=True).start()

    return frame

def write_frame(frame):
    epoch = int(time.time())
    if (epoch % 2) == 0:
        cv2.imwrite(f"img/{epoch}.jpg", frame)

capture = None
try:
    capture = cv2.VideoCapture(VIDEO_URL)
    capture.open(VIDEO_URL)

    while True:
        grabbed, frame = capture.read()
        if grabbed:
            processed_frame = process_frame(frame)
            cv2.imshow('tello-asyncio', processed_frame)
            #write_frame(frame)

        if cv2.waitKey(1) != -1:
            break

finally:
    if capture:
        capture.release()
    cv2.destroyAllWindows()