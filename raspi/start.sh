#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <destination_IP>"
    exit 1
fi

DEST_IP="$1"

# 查找所有包含"USB"的摄像头设备并选择每个设备的第一个可用设备
devices=$(v4l2-ctl --list-devices | grep -B 1 -A 2 "USB" | grep "/dev/video" | awk 'NR % 2 == 1 {print $1}')

# 为每个找到的摄像头设备启动GStreamer流水线
port=5000
for device in $devices; do
    echo "Starting stream from $device to $DEST_IP:$port"
    gst-launch-1.0 -v v4l2src device=$device ! image/jpeg,width=640,height=480,framerate=15/1 ! queue leaky=2 max-size-buffers=1 ! rtpjpegpay ! udpsink host="$DEST_IP" port=$port sync=false >/dev/null 2>&1 &
    port=$((port + 1))
done

wait
