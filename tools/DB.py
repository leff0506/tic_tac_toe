WINDOW_WIDTH = 1090
WINDOW_HEIGHT = 490
CAMERA_WIDTH = 600
CAMERA_HEIGHT = 400

BOUND_RECT_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]

#Predictor settings
CONFIDENCE = 0.5
NMS_THRESH = 0.4
CFG_FILE = "tools/finger_detection/cfg/yolov3.cfg"
WEIGHTS_FILE = "tools/finger_detection/weights/yolov3_2500.weights"
NAMES_FILE = "tools/finger_detection/data/coco.names"
RESOLUTION = 416

PLAYER_COLORS = [(255, 0, 0),(255, 255, 0)]

START_POINT_FOR_HANDS = [500,0]
HAND_IMAGE_WIDTH = 80
HAND_IMAGE_HEIGHT = 80
HAND_IMAGE_MARGIN_RIGHT = 10

SECONDS_TO_FIX = 1.0

WINDOW_TITLE = "Tic-tac-toe"