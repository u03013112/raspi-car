# networkUI.py
import socket
import tkinter as tk
from threading import Thread
import netifaces
import socketio


import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from ctrl.ping import Ping


class NetworkUI:
    def __init__(self, left_frame):
        self.websocket = None
        self.isNetworkReady = False
        self.ping_thread = None

        self.network_frame = tk.Frame(left_frame, bg="yellow", bd=1, relief="solid")

        # 获取left_frame的宽度和高度
        left_frame.update_idletasks()
        left_frame_width = left_frame.winfo_width() - 10  # 减去 10 像素，以留出左右各 5 像素的内边距
        left_frame_height = left_frame.winfo_height()

        # 使用place方法将network_frame放置在水平居中的位置，并向下偏移 5 像素以留出上方的内边距
        self.network_frame.place(relx=0.5, y=15, anchor="n", width=left_frame_width)

        self.network_info_var = tk.StringVar()
        self.local_ip_var = tk.StringVar()
        self.raspberry_ip_var = tk.StringVar()

        title_label = tk.Label(self.network_frame, text="网络状态", font=("Arial", 14, "bold"), anchor="w")
        title_label.pack(pady=(10, 5), padx=(10, 0), anchor="w")

        network_info_label = tk.Label(self.network_frame, textvariable=self.network_info_var, anchor="w")
        network_info_label.pack(pady=5, padx=(10, 0), anchor="w")
        self.network_info_var.set("请先连接树莓派")

        # 本机IP及其输入框
        local_ip_frame = tk.Frame(self.network_frame, bg="pink")
        local_ip_frame.pack(pady=(2, 2))

        local_ip_label = tk.Label(local_ip_frame, text="本机IP:", width=8, anchor="e")
        local_ip_label.pack(side="left", padx=5)
        local_ip_entry = tk.Entry(local_ip_frame, textvariable=self.local_ip_var)
        local_ip_entry.pack(side="left", padx=5)

        # 树莓派IP及其输入框
        raspberry_ip_frame = tk.Frame(self.network_frame, bg="pink")
        raspberry_ip_frame.pack(pady=(2, 2))

        raspberry_ip_label = tk.Label(raspberry_ip_frame, text="树莓派IP:", width=8, anchor="e")
        raspberry_ip_label.pack(side="left", padx=5)
        raspberry_ip_entry = tk.Entry(raspberry_ip_frame, textvariable=self.raspberry_ip_var)
        raspberry_ip_entry.pack(side="left", padx=5)

        connect_button = tk.Button(self.network_frame, text="连接", command=self.connect_to_raspberry, state="disabled")
        connect_button.pack(side="left", pady=5, padx=(0, 5))

        # 添加一个新按钮，用于重新获取本机 IP 和树莓派 IP
        refresh_ips_button = tk.Button(self.network_frame, text="刷新IP", command=lambda: Thread(target=self.get_ips).start())
        refresh_ips_button.pack(side="left", pady=5)

        Thread(target=self.get_ips).start()

        self.local_ip_var.trace("w", lambda *args: self.check_ips_and_toggle_button(connect_button))
        self.raspberry_ip_var.trace("w", lambda *args: self.check_ips_and_toggle_button(connect_button))

    def get_local_ip(self):
        self.network_info_var.set("正在获取本机IP...")
        try:
            interface_name = 'en0'
            addr = netifaces.ifaddresses(interface_name)
            local_ip = addr[netifaces.AF_INET][0]['addr']
            self.local_ip_var.set(local_ip)
        except:
            self.local_ip_var.set("获取本机IP失败")
        else:
            self.network_info_var.set("获取本机IP成功")

    def get_raspberry_ip(self):
        self.network_info_var.set("正在获取树莓派IP...")
        try:
            raspberry_ip = socket.gethostbyname("raspi.local")
            self.raspberry_ip_var.set(raspberry_ip)
        except:
            self.raspberry_ip_var.set("")
            self.network_info_var.set("树莓派IP发现失败，请手动填写")
        else:
            self.network_info_var.set("树莓派IP成功")

    def connect_to_raspberry(self):
        print("连接树莓派")
        raspberry_ip = self.raspberry_ip_var.get()
        print("树莓派 IP:", raspberry_ip)

        if self.isNetworkReady == False:
            if self.websocket == None:
                self.websocket = socketio.Client()

                @self.websocket.event
                def connect():
                    print('connection established')
                    self.network_info_var.set('连接成功')
                    self.isNetworkReady = True
                    self.network_frame.config(bg="#90EE90")

                    # 创建并启动 Ping 线程
                    self.ping_thread = Ping(self.websocket)
                    self.ping_thread.start()

                @self.websocket.event
                def disconnect():
                    print('disconnected from server')
                    self.network_info_var.set('连接断开')
                    self.isNetworkReady = False
                    self.network_frame.config(bg="yellow") 

                    # 停止 Ping 线程
                    if self.ping_thread:
                        self.ping_thread.join()
                        self.ping_thread = None
                
                @self.websocket.event
                def ping(data):
                    if self.ping_thread:
                        self.ping_thread.pong(data)
                        latency = self.ping_thread.getDt()
                        self.network_info_var.set(f"连接成功 ： {latency} ms")

            try:
                self.network_info_var.set('正在连接...')
                self.websocket.connect("http://" + raspberry_ip + ":5000")
            except Exception as e:
                print("连接失败:", e)
                self.network_info_var.set("连接失败: {}".format(e))

    def check_ips_and_toggle_button(self, connect_button):
        if self.local_ip_var.get() and self.raspberry_ip_var.get():
            connect_button.config(state="normal")
        else:
            connect_button.config(state="disabled")

    def get_ips(self):
        self.get_local_ip()
        self.get_raspberry_ip()

    def getLocalIP(self):
        return self.local_ip_var.get()
    
    def getRaspberryIP(self):
        return self.raspberry_ip_var.get()

    def exec(self, cmd):
        print("执行命令:", cmd)
        self.websocket.emit("exec", cmd)