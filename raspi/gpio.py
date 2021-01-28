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
        gpio.setup(ChLeft,gpio.OUT)
        gpio.setup(ChRight,gpio.OUT)

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

        if data['left'] == 1 :
            self.pwm.ChangeDutyCycle(10)

        if data['right'] == 1 :
            self.pwm.ChangeDutyCycle(3)
        

    