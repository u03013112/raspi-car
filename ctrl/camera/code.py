# 对上位机的编码和解码进行测试

import cv2
import numpy as np
import time

# 创建一帧720p的随机BGR图像
frame = np.random.randint(0, 256, (720, 1280, 3), dtype=np.uint8)

# 重复次数
repeat_count = 1000

# 测试MJPEG编码时间
total_encode_time = 0
for _ in range(repeat_count):
    start_time = time.time()
    ret, encoded_frame = cv2.imencode(".jpg", frame)
    end_time = time.time()
    total_encode_time += (end_time - start_time) * 1000  # 毫秒

average_encode_time = total_encode_time / repeat_count
print(f"平均MJPEG编码时间：{average_encode_time}毫秒")

# 测试MJPEG解码时间
total_decode_time = 0
for _ in range(repeat_count):
    start_time = time.time()
    decoded_frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)
    end_time = time.time()
    total_decode_time += (end_time - start_time) * 1000  # 毫秒

average_decode_time = total_decode_time / repeat_count
print(f"平均MJPEG解码时间：{average_decode_time}毫秒")
