from cv2 import cv2
import sys
import time
import threading
import numpy as np

class Camera(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.isQuit = False
        self.frame = np.zeros(480*640*3).reshape(480,640,3)

    def run(self):
        try:
            while self.isQuit == False:
                try:
                    # print('try 2 connect rtsp')
                    camera=cv2.VideoCapture("tcp://baipiao.com:6088")
                except Exception as e:
                    print('Error:',e)
                    time.sleep(1)
                    continue
                print('connected camera successed!')

                while self.isQuit == False:
                    if camera.isOpened():
                        success,frame = camera.read()
                        if success==False:
                            print('camera read err!')
                            time.sleep(1)
                            break
                        self.frame = frame
                        # print(self.frame.shape)
                    else:
                        print('camera not open!')
                        time.sleep(1)
                        break

                camera.release()
        except KeyboardInterrupt:
                self.isQuit = True
                print('received an ^C and exit.')

if __name__ == '__main__':
    camera=Camera()
    camera.start()
   