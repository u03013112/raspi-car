# -*- coding: utf-8 -*-
import sys
import keyboard
import fileinput
import time
# 这个只能放在主线程，不阻塞
class KInput:
    def __init__(self,wsc):
        self.ctrl0 = {'up':0,'down':0,'left':0,'right':0}
        self.ctrl = {'up':0,'down':0,'left':0,'right':0}
        self.wsc = wsc

    def status(self):
        return self.ctrl

    def start(self):
        def callback(event):
            if event.event_type == 'down' :
                if event.name == 'up' :
                    self.ctrl['up'] = 1
                    self.sendRaw({'ch':'up','status':'high'})
                if event.name == 'down' :
                    self.ctrl['down'] = 1
                    self.sendRaw({'ch':'down','status':'high'})
                if event.name == 'left' :
                    self.ctrl['left'] = 1
                    self.sendRaw({'ch':'left','status':'high'})
                if event.name == 'right' :
                    self.ctrl['right'] = 1
                    
            if event.event_type == 'up' :
                if event.name == 'up' :
                    self.ctrl['up'] = 0
                    self.sendRaw({'ch':'up','status':'low'})
                if event.name == 'down' :
                    self.ctrl['down'] = 0
                    self.sendRaw({'ch':'down','status':'low'})
                if event.name == 'left' :
                    self.ctrl['left'] = 0
                if event.name == 'right' :
                    self.ctrl['right'] = 0
            
            if self.ctrl0['up'] != self.ctrl['up'] or self.ctrl0['down'] != self.ctrl['down'] or self.ctrl0['left'] != self.ctrl['left'] or self.ctrl0['right'] != self.ctrl['right'] :
                self.ctrl0['up'] = self.ctrl['up'] 
                self.ctrl0['down'] = self.ctrl['down'] 
                self.ctrl0['left'] = self.ctrl['left'] 
                self.ctrl0['right'] = self.ctrl['right']
                # self.wsc.send('ctrl',self.ctrl)
                # print(self.ctrl)
        keyboard.on_press(callback, suppress=True)
        keyboard.on_release(callback)
    def sendRaw(self,data):
        self.wsc.send('ctrlRaw',data)
        print('send ',data)
if __name__ == '__main__':
    kInput = KInput('')
    kInput.start()
    time.sleep(30)

