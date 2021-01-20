# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

INT1 = 11
INT2 = 12
INT3 = 13
INT4 = 15
ENA = 16
ENB = 18

GPIO.setup(INT1,GPIO.OUT)
GPIO.setup(INT2,GPIO.OUT)
GPIO.setup(INT3,GPIO.OUT)
GPIO.setup(INT4,GPIO.OUT)
GPIO.setup(ENA,GPIO.OUT)
GPIO.setup(ENB,GPIO.OUT)

pwma = GPIO.PWM(16,80)
pwmb = GPIO.PWM(18,80)
pwma.start(90)
pwmb.start(90)
GPIO.output(INT1,GPIO.HIGH)
GPIO.output(INT2,GPIO.LOW)
GPIO.output(INT3,GPIO.HIGH)
GPIO.output(INT4,GPIO.LOW)

while 1:
        pwma.ChangeDutyCycle(90)
        pwmb.ChangeDutyCycle(90)
        time.sleep(3)
        pwma.ChangeDutyCycle(10)
        pwmb.ChangeDutyCycle(10)
        time.sleep(3)
