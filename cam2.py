from cv2 import cv2
import sys
import time
import socket
import numpy as np
import math

if __name__ =='__main__':    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    try:
            print("start connect to server ")
            s.connect(('127.0.0.1',8080))
    except socket.error:
            print("fail to connect to server")
            exit(0)
 
    print("connect success")

    s_send_buffer_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    s_receive_buffer_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

    print("client TCP send buffer size is %d" % s_send_buffer_size)
    print("client TCP receive buffer size is %d" %s_receive_buffer_size)

    t0 = time.time()
    count = 0        
    while True:
        msg = s.recv(4)
        # print("recv len is : [%d]" % len(msg))
        if len(msg) != 4:
            # print("msg len:",len(msg))
            continue
        l = int.from_bytes(msg,'big')

        t2 = s.recv(8)
        t2 = int.from_bytes(t2,'big')
        print("t2:",math.floor(time.time()*1000)-t2)

        data = s.recv(l)
        l -= len(data)
        while l >=0:
            d = s.recv(l)
            # print("len:",len(d))
            if len(d) <= 0 :
                break
            l -= len(d)
            data += d
        # print("len:",len(data))

        img_array = np.asarray(bytearray(data), dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        cv2.imshow("cam", frame)
        key = cv2.waitKey(1)
        t1 = time.time()
        count += 1
        if t1- t0 >= 1:
            print(count)
            count = 0
            t0 = t1

        
 
    s.close()