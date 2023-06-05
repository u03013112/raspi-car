import socket
import tkinter as tk
from threading import Thread

def get_local_ip(local_ip_var, network_info_var):
    network_info_var.set("正在获取本机IP...")
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
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

def connect_to_raspberry():
    print("连接树莓派")

def check_ips_and_toggle_button(local_ip_var, raspberry_ip_var, connect_button):
    if local_ip_var.get() and raspberry_ip_var.get():
        connect_button.config(state="normal")
    else:
        connect_button.config(state="disabled")

def get_ips(local_ip_var, raspberry_ip_var, network_info_var):
    get_local_ip(local_ip_var, network_info_var)
    get_raspberry_ip(raspberry_ip_var, network_info_var)

def networkUiInit(left_frame):
    network_frame = tk.Frame(left_frame, bg="pink")

    # 获取left_frame的宽度和高度
    left_frame.update_idletasks()
    left_frame_width = left_frame.winfo_width()
    left_frame_height = left_frame.winfo_height()

    # 使用place方法将network_frame放置在水平居中的位置
    network_frame.place(relx=0.5, y=10, anchor="n", width=left_frame_width)

    network_info_var = tk.StringVar()
    local_ip_var = tk.StringVar()
    raspberry_ip_var = tk.StringVar()

    title_label = tk.Label(network_frame, text="网络状态")
    title_label.pack(pady=(10, 5))

    network_info_label = tk.Label(network_frame, textvariable=network_info_var)
    network_info_label.pack(pady=5)
    network_info_var.set("请先连接树莓派")

    # 本机IP及其输入框
    local_ip_frame = tk.Frame(network_frame, bg="pink")
    local_ip_frame.pack(pady=(10, 5))

    local_ip_label = tk.Label(local_ip_frame, text="本机IP:")
    local_ip_label.pack(side="left", padx=5)
    local_ip_entry = tk.Entry(local_ip_frame, textvariable=local_ip_var)
    local_ip_entry.pack(side="left", padx=5)

    # 树莓派IP及其输入框
    raspberry_ip_frame = tk.Frame(network_frame, bg="pink")
    raspberry_ip_frame.pack(pady=(5, 10))

    raspberry_ip_label = tk.Label(raspberry_ip_frame, text="树莓派IP:")
    raspberry_ip_label.pack(side="left", padx=5)
    raspberry_ip_entry = tk.Entry(raspberry_ip_frame, textvariable=raspberry_ip_var)
    raspberry_ip_entry.pack(side="left", padx=5)

    connect_button = tk.Button(network_frame, text="连接", command=connect_to_raspberry, state="disabled")
    connect_button.pack(pady=10)

    Thread(target=get_ips, args=(local_ip_var, raspberry_ip_var, network_info_var)).start()

    local_ip_var.trace("w", lambda *args: check_ips_and_toggle_button(local_ip_var, raspberry_ip_var, connect_button))
    raspberry_ip_var.trace("w", lambda *args: check_ips_and_toggle_button(local_ip_var, raspberry_ip_var, connect_button))
