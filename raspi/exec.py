import os

class EXEC:
    def __init__(self):
        pass
    def exec(self,cmd):
        prefix = "nsenter --mount=/host/proc/1/ns/mnt "
        os.system(prefix + cmd)
    def openCamera(self):
        cmd = "raspivid -l -o tcp://0.0.0.0:8888 -hf -vf -t 0 -w 640 -h 480 -fps 15 &"
        self.exec(cmd)
    def closeCamera(self):
        self.exec("pkill raspivid")

if __name__ == '__main__':
    exec = EXEC()
    #exec.openCamera()
    exec.closeCamera()
    