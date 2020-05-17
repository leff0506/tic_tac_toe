import cv2
import tools.DB as db
class Camera:
    def __init__(self,source = 0):
        self.capture = cv2.VideoCapture(source)

    def get_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame_resized = cv2.resize(frame,(db.CAMERA_WIDTH,db.CAMERA_HEIGHT),interpolation = cv2.INTER_AREA)
            return ret,frame,frame_resized
        else:
            return ret, frame,[]
    def release(self):
        self.capture.release()