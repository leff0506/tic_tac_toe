import cv2
import tools.DB as db
import copy
import numpy as np
import time
import math


class Engine:
    def __init__(self):
        self.board = [[1, 2, 2], [2, 1, 2], [1, 2, 1]]
        self.class_barrels = [0, 0, 0, 0]
        self.hand_images = []
        self.bg_hand_images = []
        self.last_time = time.time()
        file_names = ["1.png", "2.png", "3.png", "5.png"]
        for file in file_names:
            image = cv2.imread("./images/hands/" + file, cv2.IMREAD_UNCHANGED)
            image = cv2.resize(image, (db.HAND_IMAGE_WIDTH, db.HAND_IMAGE_HEIGHT), interpolation=cv2.INTER_AREA)
            self.hand_images.append(image)

        for i in range(4):
            blank_image = np.zeros((db.HAND_IMAGE_HEIGHT, db.HAND_IMAGE_WIDTH, 4), np.uint8)
            color = (255, 255, 255)
            # color = db.BOUND_RECT_COLORS[i]
            blank_image[:, :] = (color[0], color[1], color[2], 255)

            self.bg_hand_images.append(blank_image)

    def get_canvas(self):
        canvas = np.zeros([db.WINDOW_HEIGHT, db.WINDOW_WIDTH, 4], dtype=np.uint8)
        return canvas

    def draw_backgorund(self, canvas):
        background_color = (0, 255, 255)
        cv2.rectangle(canvas, (0, 0), (10, 490), background_color, -1)
        cv2.rectangle(canvas, (160, 0), (170, 490), background_color, -1)
        cv2.rectangle(canvas, (320, 0), (330, 490), background_color, -1)
        cv2.rectangle(canvas, (480, 0), (490, 490), background_color, -1)

        cv2.rectangle(canvas, (0, 0), (490, 10), background_color, -1)
        cv2.rectangle(canvas, (0, 160), (490, 170), background_color, -1)
        cv2.rectangle(canvas, (0, 320), (490, 330), background_color, -1)
        cv2.rectangle(canvas, (0, 480), (490, 490), background_color, -1)

        cv2.rectangle(canvas, (490, 80), (1090, 90), background_color, -1)

        start = copy.copy(db.START_POINT_FOR_HANDS)
        for i in range(4):
            cv2.rectangle(canvas, (start[0] + db.HAND_IMAGE_WIDTH, start[1]),
                          (start[0] + db.HAND_IMAGE_WIDTH + db.HAND_IMAGE_MARGIN_RIGHT, start[1] + db.HAND_IMAGE_WIDTH),
                          background_color, -1)
            start[0] += db.HAND_IMAGE_WIDTH + db.HAND_IMAGE_MARGIN_RIGHT

    def draw_camera(self, canvas, frame):
        canvas[db.WINDOW_HEIGHT - db.CAMERA_HEIGHT:, db.WINDOW_WIDTH - db.CAMERA_WIDTH:, :] = cv2.cvtColor(frame,
                                                                                                           cv2.COLOR_BGR2BGRA)

    def __rotate_point(self, point, center, angle):
        vector = [0, 0]
        vector[0] = point[0] - center[0]
        vector[1] = point[1] - center[1]

        vector_result = [0, 0]
        vector_result[0] = math.cos(angle) * vector[0] - math.sin(angle) * vector[1]
        vector_result[1] = math.sin(angle) * vector[0] + math.cos(angle) * vector[1]

        result_point = [0, 0]
        result_point[0] = vector_result[0] + center[0]
        result_point[1] = vector_result[1] + center[1]

        return result_point

    def __rotate_rectangle(self, rectangle, angle):
        angle_radians = angle * math.pi / 180
        center = [0, 0]
        center[0] = (rectangle[0][0] + rectangle[2][0]) / 2
        center[1] = (rectangle[0][1] + rectangle[2][1]) / 2
        result_rectangle = []
        for point in rectangle:
            point = self.__rotate_point(point, center, angle_radians)
            result_rectangle.append(point)
        return result_rectangle

    def draw_board(self, canvas):

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 1:
                    cv2.circle(canvas, (10 + j * 160 + 75, 10 + i * 160 + 75), 65, db.PLAYER_COLORS[0], -1)
                    cv2.circle(canvas, (10 + j * 160 + 75, 10 + i * 160 + 75), 45, (0, 0, 0), -1)
                elif self.board[i][j] == 2:
                    length = 130
                    width = 20
                    center = (10 + j * 160 + 75, 10 + i * 160 + 75)
                    upper_left = [center[0] - width / 2, center[1] - length / 2]
                    upper_right = [center[0] + width / 2, center[1] - length / 2]
                    bottom_right = [center[0] + width / 2, center[1] + length / 2]
                    bottom_left = [center[0] - width / 2, center[1] + length / 2]

                    left_rectangle = self.__rotate_rectangle([upper_left,upper_right,bottom_right,bottom_left],-45)
                    right_rectangle = self.__rotate_rectangle([upper_left, upper_right, bottom_right, bottom_left], 45)
                    points = np.array([left_rectangle,right_rectangle], dtype=np.int32)
                    cv2.fillPoly(canvas, points, db.PLAYER_COLORS[1])




    def __draw_foreground_hands(self, canvas):
        start = copy.copy(db.START_POINT_FOR_HANDS)
        for i in range(4):
            added_image = cv2.bitwise_and(self.bg_hand_images[i], self.hand_images[i])
            canvas[start[1]:start[1] + db.HAND_IMAGE_WIDTH, start[0]:start[0] + db.HAND_IMAGE_WIDTH, :] = added_image
            start[0] += db.HAND_IMAGE_WIDTH + db.HAND_IMAGE_MARGIN_RIGHT

    def __create_background_hands(self):
        for i in range(4):
            image = np.zeros((db.HAND_IMAGE_HEIGHT, db.HAND_IMAGE_WIDTH, 4), np.uint8)
            color = (255, 255, 255)
            image[:, :] = (color[0], color[1], color[2], 255)
            cv2.rectangle(image, (0, db.HAND_IMAGE_HEIGHT), (
                db.HAND_IMAGE_WIDTH, db.HAND_IMAGE_HEIGHT - int(db.HAND_IMAGE_HEIGHT * self.class_barrels[i])),
                          db.BOUND_RECT_COLORS[i], -1)
            self.bg_hand_images[i] = image

    def update_barrels(self, classes):
        cur_time = time.time()
        add = (cur_time - self.last_time) / db.SECONDS_TO_FIX
        self.last_time = cur_time
        for i in range(4):
            if i in classes:
                self.class_barrels[i] = min(1.0, self.class_barrels[i] + add)
            else:
                self.class_barrels[i] = max(0, self.class_barrels[i] - add)

    def draw_hands(self, canvas):
        self.__create_background_hands()
        self.__draw_foreground_hands(canvas)
