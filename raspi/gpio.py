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
            self.pwm.ChangeDutyCycle(8)
        else if data['right'] == 1 and data['left'] == 0 :
            self.pwm.ChangeDutyCycle(4)
        else:
            self.pwm.ChangeDutyCycle(0)
            

        

    