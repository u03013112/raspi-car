import os

class EXEC:
    def __init__(self):
        pass
    def execute(self,cmd):
        prefix = "nsenter --mount=/host/proc/1/ns/mnt "
        runCmd = prefix + cmd
        print(runCmd)
        os.system(runCmd)
    def openCamera(self):
        cmd = "raspivid -l -o tcp://0.0.0.0:8888 -hf -vf -t 0 -w 640 -h 480 -fps 15 &"
        self.execute(cmd)
    def closeCamera(self):
        self.execute("pkill raspivid")

if __name__ == '__main__':
    execute = EXEC()
    #execute.openCamera()
    execute.closeCamera()
    