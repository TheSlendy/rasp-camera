import cv2
import numpy as np


class Detector:
    def __init__(self):
        self._prev_frame = None

    def detect(self, current_frame):
        frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        if self._prev_frame is None:
            self._prev_frame = frame
            return
        difference = cv2.absdiff(self._prev_frame, frame)
        self._prev_frame = frame
        kernel = np.ones((5, 5))
        thresh = cv2.threshold(difference, 20, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        areas = [cv2.contourArea(c) for c in contours]
        if len(areas) < 1:
            return False
        return True
