import cv2
VIDEO_URL = "udp://0.0.0.0:11111"

# Capture video frames from tello drone and show them
# First connect to the Tello drone Wifi and 
# then send "command" and "streamon"

# Only requirement is opencv-python install with:
# pip install opencv-python

try:
    capture = cv2.VideoCapture(VIDEO_URL)
    capture.open(VIDEO_URL)

    while True:
        grabbed, frame = capture.read()
        if grabbed:
            cv2.imshow('tello-asyncio', frame)
        if cv2.waitKey(1) != -1:
            break

finally:
    capture.release()
    cv2.destroyAllWindows()