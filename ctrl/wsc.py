import socketio
import time

class WSC:
    def __init__(self):
        sio = socketio.Client()
        self.ping = None
        @sio.event
        def connect():
            print('connection established')
            self.ready = 1

        @sio.event
        def disconnect():
            print('disconnected from server')
            self.ready = 0

        @sio.event
        def ping(data):
            # print('ping ', data)
            if self.ping != None:
                self.ping.pong(data)

        @sio.event
        def speed(data):
            if self.speed != None:
                self.speed.pong(data)

        self.ready = 0
        self.sio = sio

    def connect(self,url):
        self.sio.connect(url)

    def disconnect(self):
        self.sio.disconnect()

    def send(self,topic,data):
        if self.ready == 1:
            self.sio.emit(topic,data)

    def setPing(self,ping):
        self.ping = ping

    def setSpeed(self,speed):
        self.speed = speed

if __name__ == '__main__':
    wsc = WSC()
    wsc.connect('http://localhost:5000')
    if wsc.ready == 0 :
        time.sleep(1)
    wsc.send('ctrl','up')