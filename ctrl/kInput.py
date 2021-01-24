# -*- coding: utf-8 -*-
import sys
import keyboard
import fileinput

# 这个只能放在主线程，最后用这个阻塞主线程
class KInput:
    def __init__(self,wsc):
        self.ctrl0 = {'up':0,'down':0,'left':0,'right':0}
        self.ctrl = {'up':0,'down':0,'left':0,'right':0}
        self.wsc = wsc

    def start(self):
        try:
            while True:
                def print_event_json(event):
                    # print(event.to_json(ensure_ascii=sys.stdout.encoding != 'utf-8'))
                    sys.stdout.flush()
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
                    
                    if self.ctrl0['up'] != self.ctrl['up'] or self.ctrl0['down'] != self.ctrl['down'] or self.ctrl0['left'] != self.ctrl['left'] or self.ctrl0['right'] != self.ctrl['right'] :
                        self.ctrl0['up'] = self.ctrl['up'] 
                        self.ctrl0['down'] = self.ctrl['down'] 
                        self.ctrl0['left'] = self.ctrl['left'] 
                        self.ctrl0['right'] = self.ctrl['right']
                        self.wsc.send('ctrl',self.ctrl)
                        print(self.ctrl)

                keyboard.hook(print_event_json)
                parse_event_json = lambda line: keyboard.KeyboardEvent(**json.loads(line))
                keyboard.play(parse_event_json(line) for line in fileinput.input())
    
        except KeyboardInterrupt:
                print('received an ^C and exit.')
    