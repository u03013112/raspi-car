教程参考
https://stereopi.com/blog/stitching-360-panorama-raspberry-pi-cm3-stereopi-and-two-fisheye-cameras-step-step-guide

拍两张照，尝试做全景
fswebcam -r 1280x960 --device /dev/video0 --no-banner image3.jpg;fswebcam -r 1280x960 --device /dev/video2 --no-banner image4.jpg