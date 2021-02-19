import math
import socket
import cv2
import time
import ffmpeg
import numpy as np
import threading

# vc = cv2.VideoCapture(1)
vc = cv2.VideoCapture('/Users/u03013112/Documents/work/python/output.mp4')
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
    .input('pipe:', framerate='{}'.format(vc.get(cv2.CAP_PROP_FPS)), format='rawvideo', pix_fmt='bgr24', s='{}x{}'.format(int(vc.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    # .output('pipe:', format='rawvideo', pix_fmt='rgb24')
    .output('pipe:',format='h264', vcodec='h264', pix_fmt='nv21', **{'b:v': 2000000})
    .run_async(pipe_stdin=True,pipe_stdout=True)
)


def readThread(out,client):
    while True:
        print('-------------------------------------------------')
        data = out.read(1024)
        print(len(data))
        client.send(data)

threadRead = threading.Thread(target=readThread, args=(process.stdout,client))
threadRead.start()
# print('1-------------------------------------------------')

count = 0
while True:
    t0 = time.time()
    if vc.isOpened():
        # print('camera is opening')
        # time.sleep(0.03)
        ok, frame = vc.read()
        t1 = time.time()
        if ok == False:
            print('read err')
            continue
        else:
            # frame = cv2.resize(frame,(width, height))
            process.stdin.write(
                frame
                .astype(np.uint8)
                .tobytes()
            )
            # 中间是个多线程还是什么的，只能试试

            # print(process)
            # print(type(process.stdout))

            # while True:
            # print('-------------------------------------------------')
            # data = process.stdout.read()
            # print(len(data))
            #     client.send(data)
            #     if len(data) <128:
            #         break

            # in_bytes = process.stdout.read(width * height * 3)
            # if not in_bytes:
            #     break
            # print(len(in_bytes))
            # client.send(in_bytes)
            # data = cv2.imencode('.jpg', frame)[1]
            # client.send(data)
process.stdin.close()
process.wait()
vc.release()
