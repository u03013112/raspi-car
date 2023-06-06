# 在右侧的frame中显示摄像头的画面
# 整个右侧的frame都将显示图片
# 加一个标题，初始化为“摄像头未连接”
# 也有一个黑色实线的框，类似networkUI，更加美观
# 视频（图片）的固定分辨率为黑框中的分辨率
# 如果输入的图片分辨率不是黑框中的分辨率，那么会自动缩放
# 在右下角，添加一个控件组，显示在图片上，遮盖掉图片的一部分
# 初始状态控件组只有两个按钮，按钮的文字为“连接摄像头”和“重启摄像头”

import tkinter as tk
from PIL import Image, ImageTk

class CameraUI:
    def __init__(self, right_frame, networkUI):
        self.networkUI = networkUI
        self.camera_frame = tk.Frame(right_frame, bg="lightgray")

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
        control_frame.place(relx=1, rely=1, x=-5, y=-10, anchor="se", height=40)

        # 添加连接摄像头按钮
        connect_camera_button = tk.Button(control_frame, text="连接摄像头", command=self.connect_camera)
        connect_camera_button.pack(side="left", padx=(0, 5))

        # 添加重启摄像头按钮
        restart_camera_button = tk.Button(control_frame, text="重启摄像头", command=self.restart_camera)
        restart_camera_button.pack(side="left", padx=(0, 5))

    def connect_camera(self):
        # 连接摄像头的逻辑
        pass

    def restart_camera(self):
        # 重启摄像头的逻辑
        pass

    def update_image(self, image):
        # 更新摄像头画面
        image = self.resize_image(image, self.camera_canvas.winfo_width(), self.camera_canvas.winfo_height())
        photo = ImageTk.PhotoImage(image)
        self.camera_canvas.create_image(0, 0, image=photo, anchor="nw")
        self.camera_canvas.image = photo

    def resize_image(self, image, width, height):
        # 将图像调整为指定的宽度和高度
        return image.resize((width, height), Image.ANTIALIAS)
