# -*- coding: utf-8 -*-
import sys
import keyboard
import fileinput
import time
# 这个只能放在主线程，不阻塞
class KInput:
    def __init__(self,networkUI,cameraUI = None):
        self.ctrl0 = {'up':0,'down':0,'left':0,'right':0}
        self.ctrl = {'up':0,'down':0,'left':0,'right':0}
        self.networkUI = networkUI
        # status : l or r or 0
        self.status = '0'
        self.cameraUI = cameraUI

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
                
                
                if event.name == None and event.scan_code == 13 : 
                    # w
                    self.moveCamera(0,10)
                if event.name == None and event.scan_code == 1 :
                    # s
                    self.moveCamera(0,-10)
                if event.name == None and event.scan_code == 0 :
                    # a
                    self.moveCamera(-10,0)
                if event.name == None and event.scan_code == 2 :
                    # d
                    self.moveCamera(10,0)
                if event.name == None and event.scan_code == 15 :
                    # r
                    self.resetCamera()

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
        # self.wsc.send('ctrlRaw',data)
        try:
            self.networkUI.websocket.emit('ctrlRaw', data)  # 修改这一行
        except Exception as e:
            print('键盘事件发送失败',e)
        print('send ',data)
    
    def moveCamera(self,dx,dy):
        if self.cameraUI != None :
            self.cameraUI.current_elevation += dy
            self.cameraUI.current_azimuth += dx

            # 将角度限制在-180°到180°之间，使90度保持不变，270度转换为-90度
            if self.cameraUI.current_azimuth >= 180:
                self.cameraUI.current_azimuth -= 360
            elif self.cameraUI.current_azimuth < -180:
                self.cameraUI.current_azimuth += 360

            if self.cameraUI.current_elevation >= 180:
                self.cameraUI.current_elevation -= 360
            elif self.cameraUI.current_elevation < -180:
                self.cameraUI.current_elevation += 360
            
            # print('moveCamera',self.cameraUI.current_azimuth,self.cameraUI.current_elevation)
    def resetCamera(self):
        if self.cameraUI != None :
            self.cameraUI.current_elevation = 0
            self.cameraUI.current_azimuth = 0

if __name__ == '__main__':
    kInput = KInput('')
    kInput.start()
    time.sleep(30)

