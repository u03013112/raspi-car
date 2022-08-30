#!/bin/bash
SRC=~/Documents/leeknet/DispatcherPlatform/git/raspi-car/raspi
DST=root@192.168.1.63:/home/pi/raspi-car/
trap 'exit' INT
while :
    do
        echo '-------------------------------------------'
        fswatch -r -L -1 ${SRC}
        date
        rsync -av --exclude={"__pycache__/*"} --delete ${SRC} ${DST}
        say 啊啊啊啊
    done