import cv2
import engine.camera as cam
import random
import tools.DB as db
import time
from engine.engine import Engine
from tools.finger_detection.finger_detection import Predictor

# initial state
camera = cam.Camera()
predictor = Predictor()
game_engine = Engine()
random.seed(int(time.time()))

# who moves first
if random.randint(0,1)  == 1:
    game_engine.make_ai_random_move()
    game_engine.set_reverse_drawing()

# game loop
while camera.isOpened():
    # get frame from camera
    is_returned, frame = camera.get_frame()
    if is_returned:
        prediction = predictor.predict_draw(frame)
        frame = cv2.resize(frame, (db.CAMERA_WIDTH, db.CAMERA_HEIGHT), interpolation=cv2.INTER_AREA)
        # create canvas for drawing game
        canvas = game_engine.get_canvas()
        game_engine.draw_backgorund(canvas)
        game_engine.draw_camera(canvas,frame)

        game_engine.draw_board(canvas)

        game_engine.update_barrels(prediction)
        game_engine.draw_hands(canvas)

        game_engine.update_moves()

        # draw frame
        cv2.imshow(db.WINDOW_TITLE, canvas)
        k = cv2.waitKey(1)
        if k == 27 or cv2.getWindowProperty(db.WINDOW_TITLE, 0) < 0:  # press ESC to exit
            camera.release()
            cv2.destroyAllWindows()
            break
    else:
        break

