import math
import socket
import cv2
import time
import ffmpeg
import numpy as np
import threading

vc = cv2.VideoCapture(0)
# vc = cv2.VideoCapture('/Users/u03013112/Documents/work/python/output.mp4')
# vc.set(cv2.CAP_PROP_FPS, 60);

width = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server_address = ('0.0.0.0', 8080)
sock.bind(server_address)

lastTime=time.time()
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

process = (
    ffmpeg
    .input('pipe:', format='rawvideo', pix_fmt='bgr24', s='{}x{}'.format(int(vc.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    .output('pipe:', format='h264', **{'tune':'zerolatency'})
    .run_async(pipe_stdin=True,pipe_stdout=True)
)


def readThread(out,client):
    while True:
        data = out.read(10240)
        # print(len(data))
        client.send(data)

threadRead = threading.Thread(target=readThread, args=(process.stdout,client))
threadRead.start()

count = 0
while True:
    t0 = time.time()
    if vc.isOpened():
        ok, frame = vc.read()
        t1 = time.time()
        if ok == False:
            print('read err')
            continue
        else:
            process.stdin.write(
                frame
                .astype(np.uint8)
                .tobytes()
            )
process.stdin.close()
process.wait()
vc.release()
