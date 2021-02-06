#!/usr/bin/python3 
import tkinter as tk
from cv2 import cv2
from PIL import Image, ImageDraw, ImageFont,ImageTk

class GUI:
    def __init__(self,wsc,camera,ctrl,ping,kInput):
        self.windowW=320+960
        self.windowH=720
        self.previewW=960
        self.previewH=720

        window = tk.Tk()
        window.title("raspi car")
        window.geometry(str(self.windowW)+'x'+str(self.windowH))
        window["bg"] = "pink"
        
        self.window = window

        # left
        leftFrame = tk.Frame(window,width=320, height=720,bg='pink')
        leftFrame.pack(side='left')
        self.leftFrame = leftFrame
        
        # right
        rightFrame = tk.Frame(window,width=960, height=720,bg='white')
        rightFrame.pack(side='right')
        self.rightFrame = rightFrame

        self.wsc = wsc
        self.camera = camera
        self.ctrl = ctrl
        self.ping = ping
        self.kInput = kInput

        self.setupNetwork()
        self.setupUpdate()
        self.setupCamera()
        self.setupPreview()
    def setupUpdate(self):
        dt = 33
        # dt = 1000
        def winUpdate():
            self.window.after(dt,winUpdate)
            self.update()
        self.window.after(dt,winUpdate)
    def setupNetwork(self):
        netwrokFrame = tk.Frame(self.leftFrame,width=320, height=80,bg='#FFB6C1')
        netwrokFrame.pack()
        statusLabel=tk.Label(netwrokFrame, text='网络状态：未连接', font=('Arial', 12))
        statusLabel.place(x=10,y=15)
        #放出去，方便之后不断更改
        self.networkStatusLabel = statusLabel

        def connectButtonClicked():
            self.wsc.disconnect()
            self.wsc.connect('http://baipiao.com:6050')
            self.networkStatusLabel.configure(text='网络状态：正在重连')
            self.networkStatusLabel['bg']='white'

        connectButton = tk.Button(netwrokFrame, text='重新连接控制', font=('Arial', 12),command=connectButtonClicked)
        connectButton.place(x=10,y=40, width=100, height=20)
    def setupCamera(self):
        cameraFrame = tk.Frame(self.leftFrame,width=320, height=80,bg='pink')
        cameraFrame.pack()
        statusLabel=tk.Label(cameraFrame, text='摄像头状态：未连接', font=('Arial', 12))
        statusLabel.place(x=10,y=15)
        #放出去，方便之后不断更改
        self.cameraStatusLabel = statusLabel

        def cameraRestartButtonClicked():
            self.ctrl.restartCamera()
        # def connectButtonClicked():
        #     self.camera.connect('tcp://baipiao.com:6088')
        #     self.cameraStatusLabel.configure(text='摄像头状态：正在连接')
        #     self.cameraStatusLabel['bg']='white'
        cameraRestartButton = tk.Button(cameraFrame, text='重新启动摄像头', font=('Arial', 12),command=cameraRestartButtonClicked)
        cameraRestartButton.place(x=10,y=40, width=100, height=20)
        # connectButton = tk.Button(cameraFrame, text='连接摄像头', font=('Arial', 12),command=connectButtonClicked)
        # connectButton.place(x=10,y=60, width=100, height=20)
    def setupKInput(self):
        kInputFrame = tk.Frame(self.leftFrame,width=320, height=80,bg='pink')
        kInputFrame.pack()
        statusLabel=tk.Label(kInputFrame, text='输入状态：无输入', font=('Arial', 12))
        statusLabel.place(x=10,y=15)
        self.kInputStatusLabel = statusLabel
    def setupPreview(self):
        preview = tk.Label(self.rightFrame)
        preview['bg']='white'
        preview.place(x=0,y=0,width=960,height=720)
        self.preview = preview
    def frame2Mtk(self,frame):
        w,h,_ = frame.shape
        # 直接拉伸
        if w != self.previewW or h != self.previewH:
            frame = cv2.resize(frame,(self.previewW, self.previewH))

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=im)
        return imgtk
    def setPreview(self,frame):
        imgtk = self.frame2Mtk(frame)
        self.preview.configure(image=imgtk)
        self.preview.image = imgtk # keep a reference!

    def update(self):
        # print('update')
        if self.wsc.ready == 1:
            pingDt = 'ping:'+str(self.ping.getDt())+'ms'
            self.networkStatusLabel.configure(text='网络状态：已连接 '+ pingDt)
            self.networkStatusLabel['bg']='#00FF00'
        else:
            self.networkStatusLabel.configure(text='网络状态：未连接')
            self.networkStatusLabel['bg']='red'
        
        if self.camera.getStatus() == 0:
            fps = 'fps:'+str(self.camera.fps)
            self.cameraStatusLabel.configure(text='摄像头状态：正常 '+fps)
            self.cameraStatusLabel['bg']='#00FF00'

            self.setPreview(self.camera.frame)
        else:
            self.cameraStatusLabel.configure(text='摄像头状态：未连接'+str(self.camera.getStatus()))
            self.cameraStatusLabel['bg']='red'

        i = self.kInput.ctrl
        if i['up']==1 :
            pass
        else :
            pass
        if i['down']==1 :
            pass
        else:
            pass
        if i['left']==1 :
            pass
        else :
            pass
        if i['right']==1 :
            pass
        else:
            pass
    def show(self):
        self.window.mainloop()
