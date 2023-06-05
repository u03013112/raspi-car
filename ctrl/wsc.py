import socketio
import time

class WSC:
    def __init__(self, on_connect=None, on_disconnect=None):
        sio = socketio.Client()
        self.ping = None

        @sio.event
        def connect():
            print('connection established')
            self.ready = 1
            if on_connect:
                on_connect()

        @sio.event
        def disconnect():
            print('disconnected from server')
            self.ready = 0
            if on_disconnect:
                on_disconnect()

        @sio.event
        def ping(data):
            if self.ping:
                self.ping.pong(data)

        @sio.event
        def speed(data):
            if self.speed:
                self.speed.pong(data)

        self.ready = 0
        self.sio = sio

    def connect(self, url):
        self.sio.connect(url)

    def disconnect(self):
        self.sio.disconnect()

    def send(self, topic, data):
        if self.ready == 1:
            self.sio.emit(topic, data)

    def setPing(self, ping):
        self.ping = ping

    def setSpeed(self, speed):
        self.speed = speed

if __name__ == '__main__':
    def on_connect():
        print("Connected to the server.")

    def on_disconnect():
        print("Disconnected from the server.")

    wsc = WSC(on_connect=on_connect, on_disconnect=on_disconnect)
    wsc.connect('http://localhost:5000')
    if wsc.ready == 0:
        time.sleep(1)
    wsc.send('ctrl', 'up')
