import cv2


class Camera:
    def __init__(self, source=0):
        self.capture = cv2.VideoCapture(source)

    def get_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 1)

            return ret, frame
        else:
            return ret, []

    def isOpened(self):
        return self.capture.isOpened()

    def release(self):
        self.capture.release()
