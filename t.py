import threading
import time
def readThread(s):
    while True:
        print('-------------------------------------------------')
        time.sleep(s)
        # data = out.read()
        # print(len(data))

threadRead = threading.Thread(target=readThread,args=(1,))
threadRead.start()