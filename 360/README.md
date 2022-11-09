教程参考
https://stereopi.com/blog/stitching-360-panorama-raspberry-pi-cm3-stereopi-and-two-fisheye-cameras-step-step-guide

拍两张照，尝试做全景
fswebcam -r 1280x960 --device /dev/video0 --no-banner image0.jpg;fswebcam -r 1280x960 --device /dev/video2 --no-banner image2.jpg

fswebcam -r 1280x960 --device /dev/video0 --no-banner image0-1.jpg;fswebcam -r 1280x960 --device /dev/video2 --no-banner image2-1.jpg

uv4l --external-driver --device-name=video0 --server-option '--port=9000'


# 全景照片拼接
参考资料：https://wiki.panotools.org/Panorama_scripting_in_a_nutshell

/Applications/Hugin/tools_mac/nona -o out -m TIFF_m t.pto image0.jpg image2.jpg
/Applications/Hugin/tools_mac/enblend -o finished.tif out0000.tif out0001.tif