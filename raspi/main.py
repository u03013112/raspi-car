import eventlet
import socketio
from gpio import GPIO
from execute import EXEC

sio = socketio.Server()
app = socketio.WSGIApp(sio)
gpio = GPIO()
e = EXEC()

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def ctrl(sid, data):
    print('ctrl ', data)
    gpio.set(data)

@sio.event
def ctrlRaw(sid, data):
    print('ctrlRaw ', data)
    gpio.setRaw(data)

@sio.event
def exec(sid, data):
    print('exec ', data)
    e.execute(data['cmd'])

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':

    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)