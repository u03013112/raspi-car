
import socket
import cv2
import time

vc = cv2.VideoCapture(0)
vc.set(cv2.CAP_PROP_FPS, 60);

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
            frame = cv2.resize(frame,(320, 240))
            # cv2.imencode('.jpg', frame)[1].tofile("image.jpg")
            data = cv2.imencode('.jpg', frame)[1]
            t2 = time.time()
            client.send(data)
            t3 = time.time()
            print('read:',t1-t0,"encode:",t2-t1,"send:",t3-t2)
            count += 1
            now=time.time()
            if now - lastTime >= 1 :
                lastTime = now
                print('count:',count)
                count = 0
vc.release()
