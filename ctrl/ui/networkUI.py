import socket
import tkinter as tk
from threading import Thread
import netifaces
import socketio

# 全局变量，websocket连接
# 这里没有过度封装，所以不记录连接状态，如果希望获得连接状态，去读network_info_var
# 这里规定，当websocket连接成功时，network_info_var会被设置为"连接成功"，请直接用下面枚举做比较
websocket = None

# 枚举定义，连接成功，断开连接，连接中对应的network_info_var的值
CONNECT_STATUS_SUCCESS = "连接成功"
CONNECT_STATUS_DISCONNECT = "断开连接"
CONNECT_STATUS_ING = "连接中"

def get_local_ip(local_ip_var, network_info_var):
    network_info_var.set("正在获取本机IP...")
    try:
        interface_name = 'en0'
        addr = netifaces.ifaddresses(interface_name)
        local_ip = addr[netifaces.AF_INET][0]['addr']
        local_ip_var.set(local_ip)
    except:
        local_ip_var.set("获取本机IP失败")
    else:
        network_info_var.set("获取本机IP成功")


def get_raspberry_ip(raspberry_ip_var, network_info_var):
    network_info_var.set("正在获取树莓派IP...")
    try:
        raspberry_ip = socket.gethostbyname("raspi.local")
        raspberry_ip_var.set(raspberry_ip)
    except:
        raspberry_ip_var.set("")
        network_info_var.set("树莓派IP发现失败，请手动填写")
    else:
        network_info_var.set("树莓派IP成功")

def connect_to_raspberry(network_info_var,raspberry_ip_var):
    print("连接树莓派")
    raspberry_ip = raspberry_ip_var.get()
    print("树莓派 IP:", raspberry_ip)

    if network_info_var.get() != CONNECT_STATUS_SUCCESS:
        global websocket
        if websocket == None:
            websocket = socketio.Client()

            @websocket.event
            def connect():
                print('connection established')
                network_info_var.set(CONNECT_STATUS_SUCCESS)
                
            @websocket.event
            def disconnect():
                print('disconnected from server')
                network_info_var.set(CONNECT_STATUS_DISCONNECT)
            
        try:
            network_info_var.set(CONNECT_STATUS_ING)
            websocket.connect("http://" + raspberry_ip + ":5000")
        except Exception as e:
            print("连接失败:", e)
            network_info_var.set("连接失败: {}".format(e))

def check_ips_and_toggle_button(local_ip_var, raspberry_ip_var, connect_button):
    if local_ip_var.get() and raspberry_ip_var.get():
        connect_button.config(state="normal")
    else:
        connect_button.config(state="disabled")

def get_ips(local_ip_var, raspberry_ip_var, network_info_var):
    get_local_ip(local_ip_var, network_info_var)
    get_raspberry_ip(raspberry_ip_var, network_info_var)


def networkUiInit(left_frame):
    network_frame = tk.Frame(left_frame, bg="yellow", bd=1, relief="solid")

    # 获取left_frame的宽度和高度
    left_frame.update_idletasks()
    left_frame_width = left_frame.winfo_width() - 10  # 减去 10 像素，以留出左右各 5 像素的内边距
    left_frame_height = left_frame.winfo_height()

    # 使用place方法将network_frame放置在水平居中的位置，并向下偏移 5 像素以留出上方的内边距
    network_frame.place(relx=0.5, y=15, anchor="n", width=left_frame_width)

    network_info_var = tk.StringVar()
    local_ip_var = tk.StringVar()
    raspberry_ip_var = tk.StringVar()

    title_label = tk.Label(network_frame, text="网络状态", font=("Arial", 14, "bold"), anchor="w")
    title_label.pack(pady=(10, 5), padx=(10, 0), anchor="w")

    network_info_label = tk.Label(network_frame, textvariable=network_info_var, anchor="w")
    network_info_label.pack(pady=5, padx=(10, 0), anchor="w")
    network_info_var.set("请先连接树莓派")

    # 本机IP及其输入框
    local_ip_frame = tk.Frame(network_frame, bg="pink")
    local_ip_frame.pack(pady=(2, 2))

    local_ip_label = tk.Label(local_ip_frame, text="本机IP:", width=8, anchor="e")
    local_ip_label.pack(side="left", padx=5)
    local_ip_entry = tk.Entry(local_ip_frame, textvariable=local_ip_var)
    local_ip_entry.pack(side="left", padx=5)

    # 树莓派IP及其输入框
    raspberry_ip_frame = tk.Frame(network_frame, bg="pink")
    raspberry_ip_frame.pack(pady=(2, 2))

    raspberry_ip_label = tk.Label(raspberry_ip_frame, text="树莓派IP:", width=8, anchor="e")
    raspberry_ip_label.pack(side="left", padx=5)
    raspberry_ip_entry = tk.Entry(raspberry_ip_frame, textvariable=raspberry_ip_var)
    raspberry_ip_entry.pack(side="left", padx=5)

    connect_button = tk.Button(network_frame, text="连接", command=lambda: connect_to_raspberry(network_info_var, raspberry_ip_var), state="disabled")

    connect_button.pack(pady=5)

    Thread(target=get_ips, args=(local_ip_var, raspberry_ip_var, network_info_var)).start()

    local_ip_var.trace("w", lambda *args: check_ips_and_toggle_button(local_ip_var, raspberry_ip_var, connect_button))
    raspberry_ip_var.trace("w", lambda *args: check_ips_and_toggle_button(local_ip_var, raspberry_ip_var, connect_button))
