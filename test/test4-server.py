import socket
from cv2 import cv2
import time
import numpy as np
import ffmpeg
import threading

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

    process = (
        ffmpeg
        .input('pipe:', format='rawvideo', pix_fmt='bgr24', s='{}x{}'.format(int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        .output('pipe:', format='h264', **{'r':'20','tune':'zerolatency','preset':'ultrafast'})
        .run_async(pipe_stdin=True,pipe_stdout=True)
    )

    def readThread(out,client):
        while True:
            data = out.read(1024)
            client.send(data)

    threadRead = threading.Thread(target=readThread, args=(process.stdout,client))
    threadRead.start()

    while True:
        if camera.isOpened():
            ok, frame = camera.read()
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
    camera.release()
