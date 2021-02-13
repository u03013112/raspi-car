import math
import time
import threading

class Ping(threading.Thread):
    def __init__(self,wsc):
        threading.Thread.__init__(self)
        self.wsc = wsc
        self.time = 0
        self.lastTime = 0
        self.id = 0
        self.finishId = 0
        self.dt = 0
    def run(self):
        while True:
            self.lastTime = time.time()
            self.id += 1
            self.wsc.send('ping',{'id':self.id})
            # print('ping',self.id)
            time.sleep(1)
    def pong(self,data):
        # print('pong',self.id)
        if data['id'] == self.id :
            self.time = time.time() - self.lastTime
            self.finishId = data['id']
            self.dt = data['time'] - time.time()
    def getDt(self):
        if self.id > self.finishId + 1 :
            return '>1000'
        return math.floor(self.time*1000)
    def getRaspiTime(self):
        return time.time() + self.dt