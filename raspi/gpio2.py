# 与gpio.py的区别，这是新的电调，不再使用l298n
import RPi.GPIO as gpio

# 主电机电调pwm控制针
pwmPin = 15
# 转向舵机控制针，其实也是个pwm
servoPin = 16

class GPIO:
    def __init__(self):
        gpio.setmode(gpio.BOARD)
        # gpio.setwarnings(False)
        gpio.setup(pwmPin, gpio.OUT)
        gpio.setup(servoPin, gpio.OUT)

        self.pwm = gpio.PWM(pwmPin, 100)
        self.pwm.start(10)

        self.servo = gpio.PWM(servoPin, 100)
        self.servo.start(14)
        
    def setRaw(self,data):
        pwm = None
        if data['ch'] == 'pwm' :
            pwm = self.pwm
        if data['ch'] == 'servo' :
            pwm = self.servo
        
        if 'pwm' in data :
            pwm.ChangeDutyCycle(data['pwm'])
    