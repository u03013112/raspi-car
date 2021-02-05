#!/usr/bin/python3 
import tkinter as tk

class GUI:
    def __init__(self,wsc):
        self.windowW=320
        self.windowH=720
        self.window = tk.Tk()
        self.window.title("raspi car")
        self.window.geometry(str(self.windowW)+'x'+str(self.windowH))
        self.window["bg"] = "pink"
        
        self.wsc = wsc

        self.setupNetwork()
        self.setupUpdate()

    def setupUpdate(self):
        # dt = 33
        dt = 1000
        def winUpdate():
            self.window.after(dt,winUpdate)
            self.update()
        self.window.after(dt,winUpdate)
    def setupNetwork(self):
        frameNetwork = tk.Frame(self.window,width=self.windowW, height=200,bg='white')
        frameNetwork.pack()
        statusLabel=tk.Label(frameNetwork, text='网络状态：未连接', font=('Arial', 12))
        statusLabel.place(x=2,y=10)
        #放出去，方便之后不断更改
        self.networkStatusLabel = statusLabel

        def connectButtonClicked():
            print('did click button')
            self.wsc.disconnect()
            self.wsc.connect('http://baipiao.com:6050')
            self.networkStatusLabel.configure(text='网络状态：正在重连')

        connectButton = tk.Button(frameNetwork, text='重新连接', font=('Arial', 12),command=connectButtonClicked)
        connectButton.place(x=2,y=50, width=100, height=20)
    def update(self):
        # print('update')
        if self.wsc.ready == 1:
            self.networkStatusLabel.configure(text='网络状态：已连接')
        else
            self.networkStatusLabel.configure(text='网络状态：未连接')

    def show(self):
        self.window.mainloop()

if __name__ == '__main__':
    gui = GUI('')
    gui.show()