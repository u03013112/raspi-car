import threading
import time
import RPi.GPIO as GPIO

moerPin = 13

class Speed():
    def __init__(self):
        # 这个应该其他的线程会统一设置
        GPIO.setmode(GPIO.BOARD)         
        GPIO.setup(moerPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # 每秒重置一次
        self.lastTime = 0
        self.count = 0
        # 最近一次的速度（转每秒）
        self.lastCount = 0
    
    def timeThreadFunc(self):
        while True:
            time.sleep(1)
            self.lastCount = 0

    def speedThreadFunc(self):
        while True:
            try:
                # 会阻塞在这里，每转一圈就过去一次
                GPIO.wait_for_edge(moerPin, GPIO.FALLING)  
                self.lastCount += 1
            except:  
                pass

    # 开始测速
    def start(self):
        try:
            # t1 = threading.Thread( target=self.timeThreadFunc,args=() )
            t2 = threading.Thread( target=self.speedThreadFunc,args=() )

            # t1.start()
            t2.start()

            # t1.join()
            # t2.join()
        except:
            print ("线程终止")
            pass
        # while True:
        #     now = time.time()
        #     try:  
        #         GPIO.wait_for_edge(moerPin, GPIO.FALLING)  
                
        #     except Exception:  
        #         pass

    def getSpeed(self):
        return self.lastCount

if __name__ == '__main__':
    speed = Speed()
    speed.start()
    time.sleep(10)