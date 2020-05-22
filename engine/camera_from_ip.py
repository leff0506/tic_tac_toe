import urllib.request
import cv2
import numpy as np
import time

if __name__ == "__main__":
    URL = "http://192.168.0.101:8080/video"
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()


        cv2.imshow('IPWebcam', frame)

        cv2.waitKey(1)
