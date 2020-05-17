from __future__ import division
import time
import torch


from tools.finger_detection.util import *
from tools.finger_detection.darknet import Darknet
from tools.finger_detection.preprocess import letterbox_image

import tools.DB as db


class Predictor:
    def __init__(self):
        self.confidence = db.CONFIDENCE
        self.nms_thesh = db.NMS_THRESH
        self.classes = load_classes(db.NAMES_FILE)
        start = 0

        self.CUDA = torch.cuda.is_available()

        self.num_classes = 4

        self.CUDA = torch.cuda.is_available()


        print("Loading network.....")
        self.model = Darknet(db.CFG_FILE)
        self.model.load_weights(db.WEIGHTS_FILE)
        print("Network successfully loaded")

        self.model.net_info["height"] = db.RESOLUTION
        self.inp_dim = int(self.model.net_info["height"])
        assert self.inp_dim % 32 == 0
        assert self.inp_dim > 32

        if self.CUDA:
            self.model.cuda()
            self.model.eval()

    def prep_image(self,img, inp_dim):
        orig_im = img
        dim = orig_im.shape[1], orig_im.shape[0]
        img = (letterbox_image(orig_im, (inp_dim, inp_dim)))
        img_ = img[:, :, ::-1].transpose((2, 0, 1)).copy()
        img_ = torch.from_numpy(img_).float().div(255.0).unsqueeze(0)
        return img_, orig_im, dim

    def write(self,x, img):
        c1 = tuple(x[1:3].int())
        c2 = tuple(x[3:5].int())
        if (max(c1[0], c2[0]) - min(c1[0], c2[0])) * (max(c1[1], c2[1]) - min(c1[1], c2[1])) < 5:
            return img
        cls = int(x[-1])
        if cls > 3:
            return img
        label = "{0}".format(self.classes[cls])

        color = db.colors[cls]
        cv2.rectangle(img, c1, c2, color, 1)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
        c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
        cv2.rectangle(img, c1, c2, color, -1)
        cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225, 255, 255], 1)
        return cls

    def predict_draw(self,frame):
        self.img, self.orig_im, self.dim = self.prep_image(frame, self.inp_dim)
        self.im_dim = torch.FloatTensor(self.dim).repeat(1, 2)

        if self.CUDA:
            self.im_dim = self.im_dim.cuda()
            self. img = self.img.cuda()

        with torch.no_grad():
            self.output = self.model(Variable(self.img), self.CUDA)
        self.output = write_results(self.output, self.confidence, self.num_classes, nms=True, nms_conf=self.nms_thesh)
        if type(self.output) == int:
            return []

        self.im_dim = self.im_dim.repeat(self.output.size(0), 1)
        self.scaling_factor = torch.min(self.inp_dim / self.im_dim, 1)[0].view(-1, 1)

        self.output[:, [1, 3]] -= (self.inp_dim - self.scaling_factor * self.im_dim[:, 0].view(-1, 1)) / 2
        self.output[:, [2, 4]] -= (self.inp_dim - self.scaling_factor * self.im_dim[:, 1].view(-1, 1)) / 2

        self.output[:, 1:5] /= self.scaling_factor

        for i in range(self.output.shape[0]):
            self.output[i, [1, 3]] = torch.clamp(self.output[i, [1, 3]], 0.0, self.im_dim[i, 0])
            self.output[i, [2, 4]] = torch.clamp(self.output[i, [2, 4]], 0.0, self.im_dim[i, 1])



        result = list(map(lambda x: self.write(x, frame), (self.output)))

        if type(result[0]) == int:
            return result

        return []

# if __name__ == '__main__':
#
#     cap = cv2.VideoCapture(0)
#     assert cap.isOpened(), 'Cannot capture source'
#
#     frames = 0
#
#     predictor = Predictor()
#     start = time.time()
#     while cap.isOpened():
#
#         ret, frame = cap.read()
#
#         if not ret:
#             exit(0)
#         frame = cv2.flip(frame, 1)
#         predicted = predictor.predict_draw(frame)
#         # print(predicted)
#         cv2.imshow("frame", frame)
#
#
#
#         frames += 1
#         if time.time() - start>1:
#             print("FPS: {}".format(frames))
#             start = time.time()
#             frames =0
#
#         k = cv2.waitKey(1)
#         if k == 27:  # press ESC to exit
#             cap.release()
#             cv2.destroyAllWindows()
#             break

