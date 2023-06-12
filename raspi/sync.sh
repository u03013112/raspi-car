#!/bin/bash
raspiIP=192.168.1.104
SRC=/Users/u03013112/Documents/git/raspi-car
# DST=root@${raspiIP}:/home/pi/raspi-car/
DST=root@${raspiIP}:/home/git/
trap 'exit' INT
while :
    do
        echo '-------------------------------------------'
        fswatch -r -L -1 ${SRC}
        date
        rsync -av --exclude={"__pycache__/*"} --delete ${SRC} ${DST}
        say 啊啊啊啊
    done