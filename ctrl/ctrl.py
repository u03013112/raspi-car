# -*- coding: utf-8 -*-

class Ctrl:
    def __init__(self,wsc):
        self.wsc = wsc
    
    def restartCamera(self):
        self.wsc.send('exec',{'cmd':'pkill raspivid'})
        self.wsc.send('exec',{'cmd':'raspivid -l -o tcp://0.0.0.0:8888 -hf -vf -t 0 -w 640 -h 480 -fps 15 &'})