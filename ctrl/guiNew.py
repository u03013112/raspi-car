#!/usr/bin/python3 
import tkinter

class GUI:
    def __init__(self):
        self.windowW=1024
        self.windowH=768
        self.window = tkinter.Tk()
        self.window.title("raspi car")
        self.window.geometry()
        self.window["bg"] = "pink"
    def setupPreview(self):
        self.previewW=640
        self.previewH=480
        self.preview = tk.Label(self.window)
        self.preview.place(x=10,y=10, width=self.previewW, height=self.previewH)
    def setPreview(frame):
        w,h,_ = frame.shape
        if w != previewW or h != previewH :
            statusTextLabel.configure(text='输入分辨率不匹配')
            return
        imgtk = frame2Mtk(frame)
        preview.configure(image=imgtk)
        preview.image = imgtk # keep a reference!

    def show(self):
        self.window.mainloop()

if __name__ == '__main__':
    gui = GUI()
    gui.show()