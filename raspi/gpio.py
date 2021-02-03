import RPi.GPIO as gpio

ChUp = 11
ChDown = 12
ChLeft = 15
ChRight = 13
ChServo = 16

class GPIO:
    def __init__(self):
        gpio.setmode(gpio.BOARD)

        gpio.setup(ChUp,gpio.OUT)
        gpio.setup(ChDown,gpio.OUT)
        gpio.setup(ChLeft,gpio.OUT)
        gpio.setup(ChRight,gpio.OUT)

        gpio.output(ChUp,gpio.LOW)
        gpio.output(ChDown,gpio.LOW)
        # gpio.output(ChLeft,gpio.LOW)
        # gpio.output(ChRight,gpio.LOW)
        gpio.output(ChLeft,gpio.LOW)
        gpio.output(ChRight,gpio.HIGH)

        gpio.setup(ChServo, gpio.OUT)
        self.pwm = gpio.PWM(ChServo, 50)
        self.pwm.start(0)

    def set(self,data):
        if data['up'] == 0 :
            gpio.output(ChUp,gpio.LOW)
        else :
            gpio.output(ChUp,gpio.HIGH)
        
        if data['down'] == 0 :
            gpio.output(ChDown,gpio.LOW)
        else :
            gpio.output(ChDown,gpio.HIGH)

        if data['left'] == 1 and data['right'] == 0:
            self.pwm.ChangeDutyCycle(9)
        elif data['right'] == 1 and data['left'] == 0 :
            self.pwm.ChangeDutyCycle(5)
        else:
            self.pwm.ChangeDutyCycle(0)
            
    def setRaw(self,data):
        channel = 0
        if data['ch'] == 'up' :
            channel = ChUp
        if data['ch'] == 'down' :
            channel = ChDown
        if data['ch'] == 'left' :
            channel = ChLeft
        if data['ch'] == 'right' :
            channel = ChRight
        if data['ch'] == 'servo' :
            channel = ChServo
        
        if data['status'] == 'low' :
            gpio.output(channel,gpio.LOW)
            print(channel,'low')
        if data['status'] == 'high' :
            gpio.output(channel,gpio.HIGH)
            print(channel,'high')

        # if data['pwm'] != 0 :
        if 'pwm' in data :
            self.pwm.ChangeDutyCycle(data['pwm'])
    