# -*- coding: utf-8 -*-
import keyboard
import fileinput
import json
import sys
from wsc import WSC
import time

if __name__ =='__main__':
    wsc = WSC()
    wsc.connect('http://localhost:5000')
    
    ctrl0 = {'up':0,'down':0,'left':0,'right':0}
    ctrl = {'up':0,'down':0,'left':0,'right':0}

    while 1:
        if wsc.ready == 0 :
            time.sleep(1)
            continue
        
        def print_event_json(event):
            print(event.to_json(ensure_ascii=sys.stdout.encoding != 'utf-8'))
            sys.stdout.flush()
            if event.event_type == 'down' :
                if event.name == 'up' :
                    ctrl['up'] = 1
                if event.name == 'down' :
                    ctrl['down'] = 1
                if event.name == 'left' :
                    ctrl['left'] = 1
                if event.name == 'right' :
                    ctrl['right'] = 1
            if event.event_type == 'up' :
                if event.name == 'up' :
                    ctrl['up'] = 0
                if event.name == 'down' :
                    ctrl['down'] = 0
                if event.name == 'left' :
                    ctrl['left'] = 0
                if event.name == 'right' :
                    ctrl['right'] = 0
            
            if ctrl0['up'] != ctrl['up'] or ctrl0['down'] != ctrl['down'] or ctrl0['left'] != ctrl['left'] or ctrl0['right'] != ctrl['right'] :
                ctrl0['up'] = ctrl['up'] 
                ctrl0['down'] = ctrl['down'] 
                ctrl0['left'] = ctrl['left'] 
                ctrl0['right'] = ctrl['right']
                wsc.send('ctrl',ctrl)
        keyboard.hook(print_event_json)

        parse_event_json = lambda line: keyboard.KeyboardEvent(**json.loads(line))
        keyboard.play(parse_event_json(line) for line in fileinput.input())
    
    # wsc.send('ctrl','up')