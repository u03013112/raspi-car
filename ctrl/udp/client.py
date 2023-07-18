import cv2
import numpy as np
import socket
import struct
import time
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_heartbeat():
    while True:
        sock.sendto(b'1', ('127.0.0.1', 5000))
        time.sleep(1)

# 启动心跳发送线程
heartbeat_thread = threading.Thread(target=send_heartbeat)
heartbeat_thread.start()

frame_data = b''
frame_size = 0

# 全局变量，用于存储每秒接收的帧数
received_frame_count = 0

def print_received_frame_count():
    global received_frame_count
    while True:
        print("Frames received in the last second: ", received_frame_count)
        received_frame_count = 0
        time.sleep(1)

# 创建并启动新线程
threading.Thread(target=print_received_frame_count).start()

while True:
    data, addr = sock.recvfrom(10240)
    frame_data += data

    if frame_size == 0:
        # 尝试解析帧大小
        if len(frame_data) >= 4:
            frame_size = struct.unpack('!I', frame_data[:4])[0]
            frame_data = frame_data[4:]

    elif frame_data[-4:] == b'EOF\n':
        # 尝试解码接收到的数据
        try:
            frame = cv2.imdecode(np.frombuffer(frame_data[:-4], dtype=np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                cv2.imshow('Video', frame)
                frame_data = b''
                frame_size = 0
                received_frame_count += 1  # 增加接收到的帧数
        except Exception as e:
            pass

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
sock.close()
