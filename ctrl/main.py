# -*- coding: utf-8 -*-
import json
from wsc import WSC
import time
from kInput import KInput
from ctrl import Ctrl
from camera import Camera
from display import Display

if __name__ =='__main__':
    wsc = WSC()
    wsc.connect('http://baipiao.com:6050')
    
    # 这里应该是异步回调，图省事先
    time.sleep(1)

    ctrl = Ctrl(wsc)
    ctrl.restartCamera()

    camera = Camera()
    camera.start()

    kInput = KInput(wsc)
    kInput.start()

    display = Display(camera,kInput)
    display.start()

    