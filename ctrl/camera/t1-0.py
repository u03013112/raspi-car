# 直接测试单线程读取摄像头效率
# 未编码解码


# 结果
# 1280x720 15fps 160+ms
# 1280x720 30fps 130+ms

import cv2

cap = cv2.VideoCapture(1)
# 设置摄像头分辨率
width = 1280
height = 720
# width = 1920
# height = 1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# 设置摄像头FPS
fps = 15
cap.set(cv2.CAP_PROP_FPS, fps)

while True:
    ret, frame = cap.read()
    if not ret:
        print('未获取到帧')
        break
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break