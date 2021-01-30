# -*- coding: utf-8 -*- 

import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox
from tkinter.filedialog import *

window = tk.Tk()
window.title('raspi car') 
window.geometry('960x640')

# left
frameLeft = tk.Frame(window,width=660, height=640,bg='#999999')
frameLeft.pack(side='left')
# status
statusTextLabel=tk.Label(frameLeft, text='目前状态', font=('Arial', 12), width=35, height=1)
statusTextLabel.place(x=10,y=500)

#preview
previewW=640
previewH=480
preview = tk.Label(frameLeft)
preview.place(x=10,y=10, width=previewW, height=previewH)
# 需要转一下颜色才能显示到tk上
def frame2Mtk(frame):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(image)
    imgtk = ImageTk.PhotoImage(image=im)
    return imgtk
def setPreview(frame):
    w,h,_ = frame.shape
    if w != previewW or h != previewH :
        statusTextLabel.configure(text='输入分辨率不匹配')
        return
    imgtk = frame2Mtk(frame)
    preview.configure(image=imgtk)
    preview.image = imgtk # keep a reference!

def update():
    pass

# 关闭
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)

# 33毫秒，大致30帧
dt = 33
def winUpdate():
    window.after(dt,winUpdate)
    update()
window.after(dt,winUpdate)

# 主循环阻塞
window.mainloop()