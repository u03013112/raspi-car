import eventlet
import socketio
from gpio2 import GPIO
from execute import EXEC
import time

sio = socketio.Server()
app = socketio.WSGIApp(sio)
gpio = GPIO()
e = EXEC()

@sio.event
def connect(sid, environ):
    print('connect ', sid)

# ctrl作废，之后均使用pwm来控制
# @sio.event
# def ctrl(sid, data):
#     print('ctrl ', data)
#     gpio.set(data)

@sio.event
def ctrlRaw(sid, data):
    print('ctrlRaw ', data)
    gpio.setRaw(data)

@sio.event
def ping(sid, data):
    sendData = {}
    sendData['id'] = data['id']
    sendData['time'] = time.time()
    sio.emit('ping',sendData)

@sio.event
def exec(sid, data):
    print('exec ', data)
    e.execute(data['cmd'])

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)