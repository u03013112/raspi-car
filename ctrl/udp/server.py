# server.py
import socket
import cv2
import numpy as np

# 创建一个TCP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定到一个地址和端口
server_address = ('localhost', 10000)
print('服务器正在启动，绑定到 {}:{}'.format(*server_address))
sock.bind(server_address)

# 开始监听连接
sock.listen(1)

while True:
    print('等待连接...')
    connection, client_address = sock.accept()

    try:
        print('连接来自 {}'.format(client_address))
        data = b''
        while True:
            chunk = connection.recv(4096)
            print('收到 {} 字节'.format(len(chunk)))
            if len(chunk) < 4096:
                data += chunk
                break
            data += chunk

        if len(data) > 0:
            np_data = np.frombuffer(data, dtype=np.uint8)
            image = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

            if image is not None:
                print('收到图片')
                cv2.imshow('Received Image', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                connection.sendall('图片已接收并显示'.encode('utf-8'))
                print('已将消息发送回客户端')
            else:
                print('未收到有效图片数据')

    finally:
        connection.close()
