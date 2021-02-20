import socket
from cv2 import cv2
import time
import numpy as np

if __name__ =='__main__':
    camera=cv2.VideoCapture(0)

    print('{}x{} fps:{}'.format(
        camera.get(cv2.CAP_PROP_FRAME_WIDTH),
        camera.get(cv2.CAP_PROP_FRAME_HEIGHT),
        camera.get(cv2.CAP_PROP_POS_FRAMES)))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server_address = ('0.0.0.0', 8080)
    sock.bind(server_address)

    try:
        sock.listen(1)
    except socket.error:
        print("fail to listen on port %s" % e)
        sys.exit(1)
    while True:
        print("waiting for connection")
        client, addr = sock.accept()
        print("having a connection")
        break

    while True:
        if camera.isOpened():
            success,frame = camera.read()
            if success==False:
                print('camera read err!')
                break

            data = cv2.imencode('.jpg', frame)[1]
            client.send(len(data).to_bytes(4,byteorder='big'))
            client.send(data)
        else:
            print('camera not open!')
            break

    camera.release()
    cv2.destroyAllWindows()