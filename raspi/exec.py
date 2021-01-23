
import os

class EXEC:
    def __init__(self):
        pass
    def exec(self,cmd):
        val = os.system(cmd)
        print(val)

if __name__ == '__main__':
    exec = EXEC()
    exec.exec("nsenter --mount=/host/proc/1/ns/mnt raspivid -l -o tcp://0.0.0.0:8888 -hf -vf -t 0 -w 640 -h 480 -fps 20 &")