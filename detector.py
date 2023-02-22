import cv2
import numpy as np


class Detector:
    def __init__(self):
        self.prev_frame = None

    def detect(self, current_frame):
        frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        if self.prev_frame is None:
            self.prev_frame = frame
            return
        difference = cv2.absdiff(self.prev_frame, frame)
        self.prev_frame = frame
        kernel = np.ones((5, 5))
        difference = cv2.dilate(difference, kernel, 1)
        thresh = cv2.threshold(difference, 20, 255, cv2.THRESH_BINARY)[1]
        for i in thresh:
            if not all(elem == 0 for elem in i):
                return True
        return False
