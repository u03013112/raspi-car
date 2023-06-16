# client.py
import socket
import sys
import cv2

if len(sys.argv) != 2:
    print("用法：python client.py <图片路径>")
    sys.exit(1)

image_path = sys.argv[1]

# 创建一个TCP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 定义服务器地址和端口
server_address = ('localhost', 10000)

try:
    print('连接到服务器 {}:{}'.format(*server_address))
    sock.connect(server_address)

    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    print('发送图片：{}'.format(image_path))
    sock.sendall(image_data)

    # 等待接收服务器的响应
    print('等待接收响应...')
    data = sock.recv(4096)
    print('收到响应：{}'.format(data.decode('utf-8')))

finally:
    print('关闭套接字')
    sock.close()
