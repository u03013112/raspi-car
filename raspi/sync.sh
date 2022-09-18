#!/bin/bash
raspiIP=`arp-scan -I en0 -l|grep "dc:a6:32:f0:87:6b"|awk '{print $1}'`
SRC=~/Documents/leeknet/DispatcherPlatform/git/raspi-car/raspi
# SRC=/Users/u03013112/Documents/git/raspi-car/raspi
DST=root@${raspiIP}:/home/pi/raspi-car/
trap 'exit' INT
while :
    do
        echo '-------------------------------------------'
        fswatch -r -L -1 ${SRC}
        date
        rsync -av --exclude={"__pycache__/*"} --delete ${SRC} ${DST}
        say 啊啊啊啊
    done