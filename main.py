import cv2
import tools.camera as cam
import tools.drawable as draw
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []


def click_and_crop(event, x, y, flags, param):
    global refPt
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]


camera = cam.Camera()

while camera.capture.isOpened():
    ret, frame, frame_resized = camera.get_frame()
    if ret:

        canvas = draw.get_canvas()
        draw.draw_backgorund(canvas)
        draw.draw_camera(canvas,frame_resized)
        cv2.imshow("Camera", frame)
        cv2.imshow("Canvas", canvas)
        k = cv2.waitKey(1)
        if k == 27:  # press ESC to exit
            camera.release()
            cv2.destroyAllWindows()
            break
    else:
        break

