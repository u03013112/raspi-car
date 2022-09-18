import RPi.GPIO as gpio

# https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/

import time
# 频率
frez = 100
# 引脚
pwmPin = 16

gpio.setmode(gpio.BOARD)
gpio.setup(pwmPin, gpio.OUT)

pwm = gpio.PWM(pwmPin, frez)

pwm.start(14)
print('pwm is start')
# time.sleep(10)

pwm.ChangeDutyCycle(19)
print('cycle:',19)
time.sleep(1)

pwm.ChangeDutyCycle(14)
print('cycle:',14)
time.sleep(1)

# print('set pwm 0')
# for i in range (8,20):
#     pwm.ChangeDutyCycle(i)
#     print('cycle:',i)
#     time.sleep(1)
# print('exit')
# pwm.ChangeDutyCycle(15)
# time.sleep(10)
pwm.stop()
gpio.cleanup()