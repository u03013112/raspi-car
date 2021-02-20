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
        lStr = s.recv(4)
        if len(lStr) !=  4:
            continue
        l = int.from_bytes(lStr,'big')
        data = bytes([])
        while l > 0 :
            d = s.recv(l)
            data += d
            l -= len(d)
        img_array = np.asarray(bytearray(data), dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        cv2.imshow("test3", frame)
        key = cv2.waitKey(1)
    s.close()