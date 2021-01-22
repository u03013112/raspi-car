import RPi.gpio as gpio

ChUp = 11
ChDown = 12
ChLeft = 15
ChRight = 13

class GPIO:
    def __init__(self):
        gpio.setmode(gpio.BOARD)

        gpio.setup(ChUp,gpio.OUT)
        gpio.setup(ChDown,gpio.OUT)
        gpio.setup(ChLeft,gpio.OUT)
        gpio.setup(ChRight,gpio.OUT)

        gpio.output(ChUp,gpio.LOW)
        gpio.output(ChDown,gpio.LOW)
        gpio.output(ChLeft,gpio.LOW)
        gpio.output(ChRight,gpio.LOW)

    def set(self,date):
        if data['up'] == 1 :
            gpio.output(ChUp,gpio.LOW)
        else :
            print("up")
            gpio.output(ChUp,gpio.HIGH)
        
        if data['down'] == 1 :
            gpio.output(ChDown,gpio.LOW)
        else :
            gpio.output(ChDown,gpio.HIGH)

        if data['left'] == 1 :
            gpio.output(ChLeft,gpio.LOW)
        else :
            gpio.output(ChLeft,gpio.HIGH)

        if data['right'] == 1 :
            gpio.output(ChRight,gpio.LOW)
        else :
            gpio.output(ChRight,gpio.HIGH)
    