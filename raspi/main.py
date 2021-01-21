import eventlet
import socketio
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

ChUp = 11
ChDown = 12
ChLeft = 13
ChRight = 15

GPIO.setup(ChUp,GPIO.OUT)
GPIO.setup(ChDown,GPIO.OUT)
GPIO.setup(ChLeft,GPIO.OUT)
GPIO.setup(ChRight,GPIO.OUT)

GPIO.output(ChUp,GPIO.LOW)
GPIO.output(ChDown,GPIO.LOW)
GPIO.output(ChLeft,GPIO.LOW)
GPIO.output(ChRight,GPIO.LOW)

sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def ctrl(sid, data):
    print('message ', data)
    if data['up'] == 1 :
        GPIO.output(ChUp,GPIO.LOW)
    else :
        GPIO.output(ChUp,GPIO.HIGH)
    
    if data['down'] == 1 :
        GPIO.output(ChDown,GPIO.LOW)
    else :
        GPIO.output(ChDown,GPIO.HIGH)

    if data['left'] == 1 :
        GPIO.output(ChLeft,GPIO.LOW)
    else :
        GPIO.output(ChLeft,GPIO.HIGH)

    if data['right'] == 1 :
        GPIO.output(ChRight,GPIO.LOW)
    else :
        GPIO.output(ChRight,GPIO.HIGH)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)