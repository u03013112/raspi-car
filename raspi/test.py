import RPi.GPIO as gpio

# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/

import time
# 频率
frez = 50
# 引脚
pwmPin = 11

gpio.setmode(gpio.BOARD)
gpio.setup(pwmPin, gpio.OUT)

pwm = gpio.PWM(pwmPin, frez)

pwm.start(4)
print('pwm is start')
time.sleep(10)

print('set pwm 0')
for i in range (4,12):
    pwm.ChangeDutyCycle(i)
    print('cycle:',i)
    time.sleep(0.5)
print('exit')
pwm.ChangeDutyCycle(4)
time.sleep(10)
pwm.stop()
gpio.cleanup()