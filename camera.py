import cv2
from os import listdir, remove, path, mkdir, system
import re
from detector import Detector
from glob import glob
from client import Sender


class Camera:
    def __init__(self, video_source=0):
        self._cap = cv2.VideoCapture(video_source)
        self._detector = Detector()
        self._frame_dir = "frames"
        print("Camera Inited")
        self._sender = Sender()

    @staticmethod
    def __atoi(text):
        return int(text) if text.isdigit() else text

    def __natural_keys(self, text):
        return [self.__atoi(c) for c in re.split(r'(\d+)', text)]

    def __save_detected_motion(self, img):
        try:
            frame_list = listdir(self._frame_dir)
        except FileNotFoundError:
            mkdir(self._frame_dir)
            frame_list = listdir(self._frame_dir)
        if frame_list:
            frame_list.sort(key=self.__natural_keys)
            frame_number = re.findall(r'\d+', frame_list[-1])[0]
            cv2.imwrite(f"frames/frame#{int(frame_number) + 1}.png", img)
        else:
            cv2.imwrite("frames/frame#1.png", img)

    def __make_video(self):
        img_array = []
        for filename in glob('frames/*.png'):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)
        out = cv2.VideoWriter(f'motions/motion.avi', cv2.VideoWriter_fourcc(*'DIVX'), 5, size)
        for image in img_array:
            out.write(image)
        out.release()
        self._sender.send("motion.avi")
        for f in listdir(self._frame_dir):
            remove(path.join(self._frame_dir, f))
        remove(path.join("motions", "motion.avi"))

    def run(self):
        while True:
            _, img = self._cap.read()
            if self._detector.detect(img):
                self.__save_detected_motion(img)
                system('echo 1 | sudo tee /sys/class/leds/led0/brightness')
            else:
                system('echo 0 | sudo tee /sys/class/leds/led0/brightness')
                try:
                    frame_list = listdir(self._frame_dir)
                except FileNotFoundError:
                    mkdir(self._frame_dir)
                    frame_list = listdir(self._frame_dir)
                if frame_list:
                    print("Making video")
                    self.__make_video()
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
  
