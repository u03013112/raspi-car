from cv2 import cv2

if __name__ =='__main__':
    camera=cv2.VideoCapture(0)
    # camera.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    # camera.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    
    camera.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter.fourcc('M','J','P','G'))
    camera.set(cv2.CAP_PROP_POS_FRAMES,30)


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

            cv2.imshow("test1", frame)
            key = cv2.waitKey(1)
        else:
            print('camera not open!')
            break

    camera.release()
    cv2.destroyAllWindows()