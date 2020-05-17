import cv2
import tools.DB as db
import numpy as np


def get_canvas():
    canvas = np.zeros([db.WINDOW_HEIGHT, db.WINDOW_WIDTH, 3], dtype=np.uint8)
    return canvas


def draw_backgorund(canvas):
    background_color = (0, 255, 255)
    cv2.rectangle(canvas, (0, 0), (10, 490), background_color, -1)
    cv2.rectangle(canvas, (160, 0), (170, 490), background_color, -1)
    cv2.rectangle(canvas, (320, 0), (330, 490), background_color, -1)
    cv2.rectangle(canvas, (480, 0), (490, 490), background_color, -1)

    cv2.rectangle(canvas, (0, 0), (490, 10), background_color, -1)
    cv2.rectangle(canvas, (0, 160), (490, 170), background_color, -1)
    cv2.rectangle(canvas, (0, 320), (490, 330), background_color, -1)
    cv2.rectangle(canvas, (0, 480), (490, 490), background_color, -1)

    cv2.rectangle(canvas, (490,80),(1090,90),background_color,-1)

def draw_camera(canvas, frame):
    canvas[db.WINDOW_HEIGHT-db.CAMERA_HEIGHT:,db.WINDOW_WIDTH-db.CAMERA_WIDTH:,:] = frame