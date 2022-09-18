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
        # status : l or r or 0
        self.status = '0'

    def status(self):
        return self.ctrl

    def start(self):
        def callback(event):
            if event.event_type == 'down' :
                if event.name == 'up' :
                    self.ctrl['up'] = 1
                if event.name == 'down' :
                    self.ctrl['down'] = 1
                if event.name == 'left' :
                    self.ctrl['left'] = 1
                if event.name == 'right' :
                    self.ctrl['right'] = 1
                    
            if event.event_type == 'up' :
                if event.name == 'up' :
                    self.ctrl['up'] = 0
                if event.name == 'down' :
                    self.ctrl['down'] = 0
                if event.name == 'left' :
                    self.ctrl['left'] = 0
                if event.name == 'right' :
                    self.ctrl['right'] = 0
            
            if self.ctrl0['up'] != self.ctrl['up'] :
                self.ctrl0['up'] = self.ctrl['up']
                if self.ctrl['up'] == 1 :
                    self.sendRaw({'ch':'pwm','pwm':17,'status':'up'})
                else :
                    self.sendRaw({'ch':'pwm','pwm':15,'status':'stop'})

            if self.ctrl0['down'] != self.ctrl['down'] :
                self.ctrl0['down'] = self.ctrl['down']
                if self.ctrl['down'] == 1 :
                    self.sendRaw({'ch':'pwm','pwm':12,'status':'down'})
                else :
                    self.sendRaw({'ch':'pwm','pwm':15,'status':'stop'})
            if self.ctrl0['left'] != self.ctrl['left'] :
                self.ctrl0['left'] = self.ctrl['left']
                if self.ctrl['left'] == 1 :
                    self.sendRaw({'ch':'servo','pwm':19})
                    self.status = 'l'
                else :
                    self.sendRaw({'ch':'servo','pwm':14})
                    
            if self.ctrl0['right'] != self.ctrl['right'] :
                self.ctrl0['right'] = self.ctrl['right']
                if self.ctrl['right'] == 1 :
                    self.sendRaw({'ch':'servo','pwm':9})
                    self.status = 'r'
                else :
                    self.sendRaw({'ch':'servo','pwm':14})
                
        keyboard.on_press(callback, suppress=True)
        keyboard.on_release(callback)
    def sendRaw(self,data):
        if 'status' not in data :
            data['status'] = ''
        if 'pwm' not in data :
            if self.status == '0' :
                data['pwm'] = 0
                # 用来恢复pwm主动回轮状态
        self.wsc.send('ctrlRaw',data)
        print('send ',data)
if __name__ == '__main__':
    kInput = KInput('')
    kInput.start()
    time.sleep(30)

