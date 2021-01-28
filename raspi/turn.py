from time import sleep
import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
 
ChLeft = 15
ChRight = 13

gpio.setup(ChLeft,gpio.OUT)
gpio.setup(ChRight,gpio.OUT)

# gpio.output(ChLeft,gpio.HIGH)
# gpio.output(ChRight,gpio.LOW)

gpio.output(ChLeft,gpio.LOW)
gpio.output(ChRight,gpio.HIGH)

pin = 16
gpio.setup(pin, gpio.OUT)
pwm = gpio.PWM(pin, 50)
pwm.start(0)

for i in [0,10,20,30,40,50,60,70,80,90,100]:
    print(i)
    pwm.ChangeDutyCycle(i)
    sleep(1)

pwm.stop()
gpio.cleanup()

# def setServoAngle(servo, angle):
#     assert angle >=30 and angle <= 150
#     pwm = gpio.PWM(servo, 50)
#     pwm.start(8)
#     dutyCycle = angle / 18. + 3.
#     pwm.ChangeDutyCycle(dutyCycle)
#     sleep(0.3)
#     pwm.stop()
 
# if __name__ == '__main__':
    # import sys
    # if len(sys.argv) == 1:
    #     setServoAngle(pan, 90)
    #     setServoAngle(tilt, 90)
    # else:
    #     setServoAngle(pan, int(sys.argv[1])) # 30 ==> 90 (middle point) ==> 150
    #     setServoAngle(tilt, int(sys.argv[2])) # 30 ==> 90 (middle point) ==> 150
    # gpio.cleanup()
