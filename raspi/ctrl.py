# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

ChUp = 11
ChDown = 12
ChLeft = 13
ChRight = 15
ENA = 16
ENB = 18

GPIO.setup(ChUp,GPIO.OUT)
GPIO.setup(ChDown,GPIO.OUT)
GPIO.setup(ChLeft,GPIO.OUT)
GPIO.setup(ChRight,GPIO.OUT)
GPIO.setup(ENA,GPIO.OUT)
GPIO.setup(ENB,GPIO.OUT)

# pwma = GPIO.PWM(16,80)
# pwmb = GPIO.PWM(18,80)
# pwma.start(90)
# pwmb.start(90)
GPIO.output(ChUp,GPIO.HIGH)
GPIO.output(ChDown,GPIO.LOW)
GPIO.output(ChLeft,GPIO.HIGH)
GPIO.output(ChRight,GPIO.LOW)

# while 1:
#         pwma.ChangeDutyCycle(90)
#         pwmb.ChangeDutyCycle(90)
#         time.sleep(3)
#         pwma.ChangeDutyCycle(10)
#         pwmb.ChangeDutyCycle(10)
#         time.sleep(3)
