import cv2
import socket
import struct
import time
import threading

# 全局变量，用于存储每秒发送的帧数
frame_count = 0

def print_frame_count():
    global frame_count
    while True:
        print("Frames sent in the last second: ", frame_count)
        frame_count = 0
        time.sleep(1)

# 创建并启动新线程
threading.Thread(target=print_frame_count).start()


# 创建UDP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 5000))
sock.setblocking(0)  # 设置套接字为非阻塞模式

frame_data = b''
connected = False
timeout = 3
client_addr = None  # 保存客户端地址

def connection_watchdog():
    global connected, timeout
    while True:
        if connected:
            timeout -= 1
            if timeout <= 0:
                connected = False
                print("Disconnected")
        time.sleep(1)

# 启动连接监视线程
watchdog_thread = threading.Thread(target=connection_watchdog)
watchdog_thread.start()

# 捕获摄像头视频
cap = cv2.VideoCapture(1)

while True:
    # 尝试接收客户端消息
    try:
        data, addr = sock.recvfrom(1024)
        if data:
            connected = True
            timeout = 3
            client_addr = addr  # 保存客户端地址
    except socket.error:
        pass

    if connected and client_addr is not None:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (320, 240))
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

        frame_size = len(buffer)
        # print('frameSize:',frame_size)
        # 发送帧大小
        sock.sendto(struct.pack('!I', frame_size), client_addr)

        # 发送帧数据
        
        for i in range(0, frame_size, 1024):
            sock.sendto(buffer[i:i+1024], client_addr)
        # sock.sendto(buffer, client_addr)

        # 发送结束标记
        sock.sendto(b'EOF\n', client_addr)

        frame_count += 1

cap.release()
cv2.destroyAllWindows()
sock.close()
