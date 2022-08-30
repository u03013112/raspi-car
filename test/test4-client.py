from cv2 import cv2

if __name__ =='__main__':
    # camera=cv2.VideoCapture('tcp://127.0.0.1:8080')
    camera=cv2.VideoCapture('tcp://192.168.1.59:8080')

    print('{}x{} fps:{}'.format(
        camera.get(cv2.CAP_PROP_FRAME_WIDTH),
        camera.get(cv2.CAP_PROP_FRAME_HEIGHT),
        camera.get(cv2.CAP_PROP_POS_FRAMES)))
    while True:
        if camera.isOpened():
            success,frame = camera.read()
            if success==False:
                print('camera read err!')
                break

            cv2.imshow("test4", frame)
            key = cv2.waitKey(1)
        else:
            print('camera not open!')
            break

    camera.release()
    cv2.destroyAllWindows()