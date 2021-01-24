# -*- coding: utf-8 -*-
import json
from wsc import WSC
import time
from kInput import KInput


if __name__ =='__main__':
    wsc = WSC()
    wsc.connect('http://baipiao.com:6050')
    
    kInput = KInput(wsc)
    kInput.start()