from cv2 import cv2
import sys
import time

#变成一个纯粹的监视器
if __name__ =='__main__':
    if len(sys.argv) <2:
            print('input ip of netcam!')
            exit()

    while True:
        try:
            print('try 2 connect rtsp')
            camera=cv2.VideoCapture(sys.argv[1])
        except Exception as e:
            print('Error:',e)
            continue
        print('connected '+sys.argv[1]+' successed!')

        while True:
            if camera.isOpened():
                success,frame = camera.read()
                t0 = time.time()
                if success==False:
                    print('camera read err!')
                    break

                cv2.imshow("cam", frame)
                t1 = time.time()
                # print(t1-t0)
                key = cv2.waitKey(1)
            else:
                print('camera not open!')
                break

        camera.release()
        cv2.destroyAllWindows()