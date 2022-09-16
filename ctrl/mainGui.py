# -*- coding: utf-8 -*-
import json
from wsc import WSC
import time
from kInput import KInput
from ctrl import Ctrl
from camera import Camera
from ping import Ping
from guiNew import GUI

if __name__ =='__main__':
    wsc = WSC()
    # wsc.connect('http://baipiao.com:6050')
    wsc.connect('http://192.168.1.59:5000')
    
    # # 这里应该是异步回调，图省事先
    time.sleep(1)

    ctrl = Ctrl(wsc)
    ctrl.restartCamera()

    ping = Ping(wsc)
    ping.start()
    wsc.setPing(ping)

    camera = Camera()
    camera.start()

    kInput = KInput(wsc)
    kInput.start()

    gui = GUI(wsc,camera,ctrl,ping,kInput)
    gui.show()