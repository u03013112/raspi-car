# 在右侧的frame中显示摄像头的画面
# 整个右侧的frame都将显示图片
# 加一个标题，初始化为“摄像头未连接”
# 也有一个黑色实线的框，类似networkUI，更加美观
# 视频（图片）的固定分辨率为黑框中的分辨率
# 如果输入的图片分辨率不是黑框中的分辨率，那么会自动缩放
# 在右下角，添加一个控件组，显示在图片上，遮盖掉图片的一部分
# 初始状态控件组只有两个按钮，按钮的文字为“连接摄像头”和“重启摄像头”

# 得到目前的现实时间
# 原始模式30ms左右
# 等距模式50ms左右
# 等角模式60ms左右

import tkinter as tk
import tkinter.messagebox as messagebox

from PIL import Image, ImageTk
import threading
import gi
import numpy as np
import cv2
import os
import time

from u0_stitcher.stitcher import Stitcher
from u0_stitcher.errors import CircleCenterNotCalibratedException, StitchNotCalibratedException
from Equirec2PerspecNew import Equirectangular


gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import Gst

Gst.init(None)

gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import Gst

Gst.init(None)

# 暂时没想好名字，就叫App吧
# 视频流接收器
class App:
    def __init__(self, port):
        self.frame = None
        self.pipeline = self.create_pipeline(port)
        self.lastTime = 0
        # self.fps = 0
        self.timestamp = 0
        

    def on_new_sample(self, sink):
        if __debug__:
            self.timestamp = time.time()

        # print("on_new_sample")
        sample = sink.emit("pull-sample")
        buffer = sample.get_buffer()
        caps = sample.get_caps()
        width = caps.get_structure(0).get_value("width")
        height = caps.get_structure(0).get_value("height")

        success, mapinfo = buffer.map(Gst.MapFlags.READ)
        if success:
            self.frame = np.ndarray((height, width, 3), buffer=mapinfo.data, dtype=np.uint8)
            buffer.unmap(mapinfo)

        return Gst.FlowReturn.OK

    def create_pipeline(self, port):
        pipeline = Gst.parse_launch(f"udpsrc port={port} ! application/x-rtp,media=video,payload=26,clock-rate=90000,encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! videoconvert ! video/x-raw,format=RGB ! queue max-size-buffers=1 max-size-time=0 ! appsink name=sink emit-signals=True sync=False")

        sink = pipeline.get_by_name("sink")
        sink.connect("new-sample", self.on_new_sample)
        return pipeline

class CameraUI:
    def __init__(self, right_frame, networkUI):
        self.networkUI = networkUI
        self.camera_frame = tk.Frame(right_frame, bg="lightgray")

        self.mode = 'original'
        self.pano = Stitcher()
        self.circle_center_exception = 0
        self.stitch_exception = 0
        # calibImage 只用于校准时候的图片
        self.calibImage = None
        self.check_exceptions()

        self.app1 = App(5000)
        self.app2 = App(5001)

        self.app1.pipeline.set_state(Gst.State.PLAYING)
        self.app2.pipeline.set_state(Gst.State.PLAYING)

        # 在这里，我们添加了两个变量来存储当前的方位角和高度角，为了等角投影
        self.current_azimuth = 0
        self.current_elevation = 0

        # 获取right_frame的宽度和高度
        right_frame.update_idletasks()
        right_frame_width = right_frame.winfo_width() - 10  # 减去 10 像素，以留出左右各 5 像素的内边距
        right_frame_height = right_frame.winfo_height()

        # 使用place方法将camera_frame放置在水平居中的位置，并向下偏移 5 像素以留出上方的内边距
        self.camera_frame.place(relx=0.5, y=5, anchor="n", width=right_frame_width, height=right_frame_height)

        self.camera_title_var = tk.StringVar()
        self.camera_title_var.set("摄像头未连接")

        title_label = tk.Label(self.camera_frame, textvariable=self.camera_title_var, font=("Arial", 14, "bold"), anchor="w", bg="lightgray", fg="black")
        title_label.pack(pady=(10, 0), padx=(10, 0), anchor="w")

        # 创建一个Canvas用于显示摄像头画面
        self.camera_canvas = tk.Canvas(self.camera_frame, width=right_frame_width, height=right_frame_height - 50, bg="white", bd=1, relief="solid")
        self.camera_canvas.pack(pady=(5, 5))

        # 创建控件组
        control_frame = tk.Frame(self.camera_frame, bg="lightgray")
        control_frame.place(relx=1, rely=1, x=-5, y=-10, anchor="se", height=120)

        # 第一行
        row1_frame = tk.Frame(control_frame, bg="lightgray")
        row1_frame.pack(side="top", pady=(0, 5))

        # 添加重启摄像头按钮
        restart_camera_button = tk.Button(row1_frame, text="重启摄像头", command=self.restart_camera)
        restart_camera_button.pack(side="left", padx=(0, 5))

        # 第二行
        row2_frame = tk.Frame(control_frame, bg="lightgray")
        row2_frame.pack(side="top", pady=(0, 5))

        # 添加各种模式按钮
        originalModeButton = tk.Button(row2_frame, text="原始模式", command=lambda: self.changeMode("original"))
        originalModeButton.pack(side="left", padx=(0, 5))

        eqDistanceModeButton = tk.Button(row2_frame, text="等距模式", command=lambda: self.changeMode("equal_distance_projection"))
        eqDistanceModeButton.pack(side="left", padx=(0, 5))

        eqAngleModeButton = tk.Button(row2_frame, text="等角模式", command=lambda: self.changeMode("equal_angle_projection"))
        eqAngleModeButton.pack(side="left", padx=(0, 5))

        # 第三行
        row3_frame = tk.Frame(control_frame, bg="lightgray")
        row3_frame.pack(side="top", pady=(0, 5))

        # 添加切换主摄像头按钮
        switch_camera_button = tk.Button(row3_frame, text="切换主摄像头", command=self.switch_camera)
        switch_camera_button.pack(side="left", padx=(0, 5))

        # 添加重新校准按钮
        calibrate_button = tk.Button(row3_frame, text="重新校准", command=self.calibrate)
        calibrate_button.pack(side="left", padx=(0, 5))

        # 启动一个新的线程来执行update_frames方法
        update_frames_thread = threading.Thread(target=self.update_frames)
        update_frames_thread.daemon = True
        update_frames_thread.start()

    def close(self):
        # 停止GStreamer管道
        self.app1.pipeline.set_state(Gst.State.NULL)
        self.app2.pipeline.set_state(Gst.State.NULL)

    def changeMode(self,mode):
        self.mode = mode

    def switch_camera(self):
        if self.pano.config['img1'] == 'left':
            self.pano.calibMainCamera('right')
        else:
            self.pano.calibMainCamera('left')

    def calibrate(self):
        self.stitch_exception = 1

    def restart_camera(self):
        # 执行 bash /home/git/raspi-car/raspi/start.sh 192.168.1.101
        self.networkUI.websocket.emit('exec',{'cmd':'bash /home/git/raspi-car/raspi/start.sh 10.0.0.100 &'})
        

    def update_image(self, image):
        # 更新摄像头画面
        photo = ImageTk.PhotoImage(image)
        self.camera_canvas.create_image(0, 0, image=photo, anchor="nw")
        self.camera_canvas.image = photo

    def resize_image_opencv(self,image, target_width, target_height):
        original_height, original_width = image.shape[:2]
        aspect_ratio = float(original_width) / float(original_height)
        if target_width / aspect_ratio < target_height:
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:
            new_width = int(target_height * aspect_ratio)
            new_height = target_height

        return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    def check_exceptions(self):
        if self.circle_center_exception:
            # 弹出警告窗口
            messagebox.showwarning("Warning", "需要校准圆心")
            # 处理异常
            self.pano.calibCircleCenter(self.calibImage)
            # 重置异常状态
            self.circle_center_exception = 0

        # 在1秒后再次运行此函数
        self.camera_frame.after(1000, self.check_exceptions)


    def update_frames(self):
        # 此函数整个就在一个分线程中运行，后台尝试更新界面
        # 请不要在此线程中尝试调用imshow等方法，因为这些方法必须在主线程中调用

        app1 = self.app1
        app2 = self.app2

        if __debug__:
            imgTimestamp1 = 0
            imgTimestamp2 = 0

            lastTime = 0
            fps = 0
            totalTime = 0
            totalTimeA = 0
            totalTimeB = 0
            totalTimeC = 0

        while True:
            image = None
            if app1.frame is None and app2.frame is None:
                self.camera_title_var.set("摄像头未连接")
                image = None
            elif app1.frame is not None and app2.frame is not None:
                self.camera_title_var.set("摄像头已连接")
                image = np.hstack((app1.frame, app2.frame))
                if __debug__:
                    imgTimestamp1 = app1.timestamp
                    imgTimestamp2 = app2.timestamp

            elif app1.frame is not None:
                self.camera_title_var.set("摄像头 1 已连接")
                image = app1.frame
                if __debug__:
                    if imgTimestamp1 == app1.timestamp:
                        continue                        
                    imgTimestamp1 = app1.timestamp
                    # print('A:%.2fms'%((time.time()-imgTimestamp1)*1000))
                    dtA = time.time()-imgTimestamp1

            elif app2.frame is not None:
                self.camera_title_var.set("摄像头 2 已连接")
                image = app2.frame
            
            if image is not None:
                if self.mode == 'original':
                    retFrame = image
                elif self.mode == 'equal_distance_projection' or self.mode == 'equal_angle_projection':
                    # 下面这些except暂未测试，可能会有bug
                    try:
                        retFrame = self.pano.stitch(image)
                    except CircleCenterNotCalibratedException as e:
                        # print(e)
                        # self.pano.calibCircleCenter(image)
                        self.calibImage = image
                        self.circle_center_exception = 1
                        time.sleep(1)
                    except StitchNotCalibratedException as e:
                        print(e)
                        self.pano.calibStitch(image)
                    else:
                        if self.mode == 'equal_angle_projection':
                            equ = Equirectangular(retFrame)
                            retFrame = equ.GetPerspective(120,90, self.current_azimuth, self.current_elevation, 300, 400)

                            # 在右上角绘制半透明圆和箭头
                            circle_radius = 30
                            circle_center = (retFrame.shape[1] - circle_radius - 10, circle_radius + 10)
                            arrow_length = 20
                            arrow_tip = (circle_center[0], circle_center[1] - arrow_length)

                            # 创建一个与retFrame大小相同的透明图层
                            overlay = retFrame.copy()

                            # 在透明图层上绘制圆形
                            cv2.circle(overlay, circle_center, circle_radius, (255, 255, 255), -1)

                            # 将透明图层添加到retFrame上，设置透明度为0.5
                            retFrame = cv2.addWeighted(overlay, 0.5, retFrame, 0.5, 0)

                            # 在retFrame上绘制箭头
                            retFrame = cv2.arrowedLine(retFrame, circle_center, arrow_tip, (0, 0, 0), 2)

                            # 绘制半透明扇形
                            angle_start = 90 - self.current_azimuth - 60
                            angle_end = 90 - self.current_azimuth + 60

                            # 创建一个与retFrame大小相同的透明图层
                            overlay = retFrame.copy()

                            # 在透明图层上绘制扇形
                            for angle in np.arange(angle_start, angle_end, 1):
                                x = int(circle_center[0] + circle_radius * np.cos(np.radians(angle)))
                                y = int(circle_center[1] - circle_radius * np.sin(np.radians(angle)))
                                cv2.line(overlay, circle_center, (x, y), (0, 255, 0), 2)

                            # 将透明图层添加到retFrame上，设置透明度为0.5
                            retFrame = cv2.addWeighted(overlay, 0.5, retFrame, 0.5, 0)

                            # 添加水平角度和垂直角度文本
                            angle_text_h = "H: {:.1f} deg".format(self.current_azimuth)
                            angle_text_v = "V: {:.1f} deg".format(self.current_elevation)
                            retFrame = cv2.putText(retFrame, angle_text_h, (circle_center[0] - circle_radius, circle_center[1] + circle_radius + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
                            retFrame = cv2.putText(retFrame, angle_text_v, (circle_center[0] - circle_radius, circle_center[1] + circle_radius + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
                
                    if self.stitch_exception == 1:
                        self.stitch_exception = 0
                        try:
                            print('尝试重校准')
                            self.pano.calibStitch(image)
                        except:
                            # 手动校准可能会由于一些原因导致校准失败，这里不做处理
                            pass
                try:
                    retFrame = self.resize_image_opencv(retFrame, self.camera_canvas.winfo_width(), self.camera_canvas.winfo_height())
                    retFrame = Image.fromarray(retFrame)
                except Exception as e:
                    # 这里是校准的过程中会出现一些不可预料的结果，可能无法有效的转换为Image
                    print('转换为Image失败:',e)
                    pass
                else:
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    dtB = time.time()-imgTimestamp1
                    self.update_image(retFrame)
                    dtC = time.time()-imgTimestamp1
                    if __debug__:
                        # dt = time.time() - min(imgTimestamp1, imgTimestamp2)
                        dt = time.time() - imgTimestamp1
                        # print('%.1f ms'%(dt*1000))

                        if lastTime == 0:
                            lastTime = time.time()
                            fps += 1
                        else:
                            now = time.time()
                            # if now - lastTime > 1:
                            #     lastTime = now
                            #     print('fps:', fps, 'avg time:%.1f ms'%(float(totalTime) / float(fps) * 1000))
                            #     # print('avg timeA:%.1f ms'%(float(totalTimeA) / float(fps) * 1000))
                            #     # print('avg timeB:%.1f ms'%(float(totalTimeB) / float(fps) * 1000))
                            #     # print('avg timeC:%.1f ms'%(float(totalTimeC) / float(fps) * 1000))
                            #     fps = 0
                            #     totalTime = 0
                            #     # totalTimeA = 0
                            #     # totalTimeB = 0
                            #     # totalTimeC = 0
                            # else:
                            #     fps += 1
                            #     totalTime += dt
                            #     # totalTimeA += dtA
                            #     # totalTimeB += dtB
                            #     # totalTimeC += dtC


                            
            else:
                time.sleep(1)

            