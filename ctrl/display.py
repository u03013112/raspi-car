# -*- coding: utf-8 -*-
from cv2 import cv2
import numpy as np

# 这个必须在主线程，阻塞在最后
class Display:
    def __init__(self,camera):
        self.camera = camera
        
    def start(self):
        while True:
            if self.camera :
                frame = self.camera.frame
                cv2.imshow("cam", frame)
                key = cv2.waitKey(1)