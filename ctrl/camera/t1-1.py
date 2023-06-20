# 直接测试单线程读取摄像头效率
# mjpg 编码

# 结果
# 1280x720 30fps 80~130+ms 好像还有一些波动，波动范围超出了fps的范围

import cv2

cap = cv2.VideoCapture(0)
# 设置摄像头分辨率
width = 1280
height = 720

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# 设置摄像头FPS
fps = 30
cap.set(cv2.CAP_PROP_FPS, fps)

# 设置摄像头属性，使用MJPEG编码
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

while True:
    ret, frame = cap.read()
    if not ret:
        print('未获取到帧')
        break

    cv2.imshow('Video', frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
