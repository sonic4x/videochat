import cv2
import numpy
import io
from PIL import Image
import numpy as np
class VideoFeed:

    def __init__(self,mode=1,name="w1",capture=1):
        print(name)
        self.camera_index = 0
        self.name = name
        if capture == 1:
            self.cam = cv2.VideoCapture(self.camera_index)
        elif capture == 2:
            self.cam = cv2.VideoCapture("/home/liang/Videos/29_2_w_waitingzone.mp4")

    def get_frame(self):
        ret_val, img = self.cam.read()
        c = cv2.waitKey(1)
        if (c == "n"): #in "n" key is pressed while the popup window is in focus
            self.camera_index += 1 #try the next camera index
            self.cam = cv2.VideoCapture(self.camera_index)
            if not self.cam: #if the next camera index didn't work, reset to 0.
                self.camera_index = 0
                self.cam = cv2.VideoCapture(self.camera_index)

        #cv2.imshow('my webcam', img)
        cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)
        b = io.BytesIO()
        pil_im.save(b, 'jpeg')
        im_bytes = b.getvalue()
        return im_bytes
    
    def get_pic(self):
        #cv2.imshow('my webcam', img)
        im = Image.open("/home/liang/Pictures/right_curve_road.png")
        # cv_image = cv2.cvtColor(numpy.array(im), cv2.COLOR_RGB2BGR)
        # cv2.imshow(self.name, cv_image)
            # im.rotate(45).show()
        # cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # pil_im = Image.fromarray(cv2_im)
        b = io.BytesIO()
        im.save(b, format='PNG')
        im_bytes = b.getvalue()

        # pil_bytes = io.BytesIO(im_bytes)
        # pil_image = Image.open(pil_bytes)
        # pil_image.show()
        # cv_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
        # cv2.imshow(self.name, cv_image)

        return im_bytes

    def set_frame(self, frame_bytes):
        pil_bytes = io.BytesIO(frame_bytes)
        pil_image = Image.open(pil_bytes)
        pil_image.show()

        print("set_frame")

    def get_pic_cv_version(self):
        cv2_im = cv2.imread("/home/liang/Pictures/right_curve_road.png")
        cv2_im = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)

        b = io.BytesIO()
        im_bytes = b.getvalue()
        return im_bytes

    def set_frame_cv_version(self, frame_bytes):
        pil_bytes = io.BytesIO(frame_bytes)
        pil_image = Image.open(pil_bytes)
        pil_image.show()

        print("set_frame")

    def testcv2PIL(self):
        # convert cv2 -> PIL
        cv2_im = cv2.imread("/home/liang/Pictures/right_curve_road.png")
        cv2_im = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)
        pil_im.show()

    def testPIL2cv(self):
        pil_im = Image.open("/home/liang/Pictures/right_curve_road.png")
        im_np = numpy.array(pil_im)
        im_cv2 = cv2.cvtColor(im_np, cv2.COLOR_RGB2BGR)
        cv2.imshow(self.name, im_cv2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def get_video_frame(self):
        success,img = self.cam.read()
        cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)
        b = io.BytesIO()
        pil_im.save(b, 'jpeg')
        im_bytes = b.getvalue()
        return im_bytes
    
    def set_video_frame(self, frame_bytes):
        pil_bytes = io.BytesIO(frame_bytes)
        pil_image = Image.open(pil_bytes)
        cv_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
        cv2.imshow(self.name, cv_image)
        if cv2.waitKey(1) & 0xFF == 27:  # if ESC pressed during wait 1ms
            cv2.destroyWindow(self.name)

if __name__=="__main__":
    vf = VideoFeed(1,"test",1)
    # while 1:
    #     m = vf.get_frame()
    #     vf.set_frame(m)
    vf.testPIL2cv()
