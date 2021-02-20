import socket
from cv2 import cv2
import numpy as np

if __name__ =='__main__':    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    try:
        print("start connect to server ")
        s.connect(('127.0.0.1',8080))
    except socket.error:
        print("fail to connect to server")
        exit(0)
 
    print("connect success")

    while True:
        l = 921600
        data = bytes([])
        while l > 0 :
            d = s.recv(l)
            data += d
            l -= len(d)

        frame = np.frombuffer(data, dtype=np.uint8).reshape(480,640,3)
        cv2.imshow("test2", frame)
        key = cv2.waitKey(1)
    s.close()