
from subprocess import call

class EXEC:
    def __init__(self,w=640,h=480,fps=15):
        self.w = w
        self.h = h
        self.fps = fps

    def exec(self,cmd):
        prefix = "nsenter --mount=/host/proc/1/ns/mnt "
        call(prefix + cmd) 
        # shell=True
    def openCamera(self):
        cmd = "raspivid -l -o tcp://0.0.0.0:8888 -hf -vf -t 0 -w "+self.w+" -h "+self.h+" -fps "+self.fps +" &"
        self.exec(cmd)
    def closeCamera(self):
        self.exec("pkill raspivid")

if __name__ == '__main__':
    exec = EXEC()
    