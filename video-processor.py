#!/usr/bin/env python3

import time
import cv2
import boto3
import numpy
from threading import Thread

VIDEO_URL = "udp://0.0.0.0:11111"

rekognition = boto3.client('rekognition', region_name='us-east-2')

# Capture video frames from tello drone, detect labels and show them
# First connect to the Tello drone Wifi and 
# then send "command" and "streamon"

# Only requirements are opencv-python and boto3 install with:
# pip install opencv-python boto3

def get_searched_items():
    items = set([])
    with open('video-searched-items.txt') as f:
        items = set([item.lower().strip() for item in f.readline().split(",")])

    return items

def detect_labels(frame):
    searched_items = get_searched_items()
    image_encoded = cv2.imencode('.jpg', frame)[1]
    image_bytes = (numpy.array(image_encoded)).tobytes()
    response = rekognition.detect_labels(
        Image={'Bytes': image_bytes},
        MinConfidence=77.5
    )
    print()
    for label in response['Labels']:
        label_name = label['Name']
        print(label_name, end =" ")
        if label_name.lower().strip() in searched_items:
            print(f"\n\nFound: {label_name}!!!\n")
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

    

def write_frame(frame):
    epoch = int(time.time())
    if (epoch % 2) == 0:
        cv2.imwrite(f"img/{epoch}.jpg", frame)


def process_frame(frame, start_time):
    now = time.time()
    if now - start_time > 0.8:
        start_time = now
        Thread(target=detect_labels, args=(frame,), daemon=True).start()

    return start_time


capture = None
try:
    capture = cv2.VideoCapture(VIDEO_URL)
    capture.open(VIDEO_URL)

    start_time = time.time()
    while True:
        grabbed, frame = capture.read()
        if grabbed:
            start_time = process_frame(frame, start_time)
            cv2.imshow('tello-asyncio', frame)

        if cv2.waitKey(1) != -1:
            break

finally:
    if capture:
        capture.release()
    cv2.destroyAllWindows()
