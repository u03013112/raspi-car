# 和不分线程的结果类似差不多，看起来这个线程效果不明显


import cv2
import threading

class VideoCaptureThread(threading.Thread):
    def __init__(self, src=0):
        super(VideoCaptureThread, self).__init__()
        self.cap = cv2.VideoCapture(src)
        # 设置摄像头分辨率
        width = 1280
        height = 720

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # 设置摄像头FPS
        fps = 30
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.current_frame = None
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break
            self.current_frame = frame

    def get_frame(self):
        return self.current_frame

    def stop(self):
        self.running = False
        self.cap.release()

def main():
    video_thread = VideoCaptureThread(0)
    video_thread.start()

    while True:
        frame = video_thread.get_frame()
        if frame is not None:
            # # 左右反转
            # frame = cv2.flip(frame, 1)
            cv2.imshow('Video', frame)

        key = cv2.waitKey(1)
        if key == 27:  # ESC
            break

    video_thread.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
