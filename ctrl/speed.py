# 获得转速，从raspi获得
import time
import threading

class Speed(threading.Thread):
    def __init__(self,wsc):
        threading.Thread.__init__(self)
        self.wsc = wsc
        self.speed = 0
    def run(self):
        while True:
            # self.wsc.send('speed',{})
            self.wsc.emit('speed',{})  # 修改这一行
            time.sleep(0.5)
    def pong(self,data):
        self.speed = data['speed']