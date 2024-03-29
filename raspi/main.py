import eventlet
import socketio
from execute import EXEC
import time

sio = socketio.Server()
app = socketio.WSGIApp(sio)
e = EXEC()

try:
    from gpio2 import GPIO
    gpio = GPIO()
    from speed import Speed
    s = Speed()
    s.start()
except Exception as e:
    print(e)

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

@sio.event
def speed(sid, data):
    # print('speed ', data)
    r = s.getSpeed()
    sendData = {'speed':r}
    # print(sendData)
    sio.emit('speed',sendData)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)