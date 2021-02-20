为了测试视频流传输所效率

`测试方式`：
1、opencv 读取摄像头数据 -> opencv 播放
2、opencv 读取摄像头数据 -> tcp发送 -> opencv 播放 (验证网络发送效率折损，纯本地无延迟)
3、opencv 读取摄像头数据 -> 简单处理 -> tcp发送 -> opencv 播放 （验证处理速度，比较值的验证的是压缩图片和压缩流）

4、利用其它库读取播放，比如ffmpeg，这个测试暂时感觉没有太大意义

`测试工具`：
利用一个30块的摄像头，fps最高只有17帧左右，低帧速率会有一定程度的影响时延。

`测试结果`：
1、130ms以内，同步性高
2、150ms以内，同步性感受差不多，可能python代码确实效率有限
3、图片压缩成jpg，130ms超稳定，甚至比2还要稳定，可能是read的次数比较少导致的
3、视频流压缩成h264，进入300ms，明显感受到滞后感，h264配置可能可以在调整

目前h264选用参数：
-tune zerolatency，应该类似：
--bframes 0 --force-cfr --no-mbtree
--sync-lookahead 0 --sliced-threads
--rc-lookahead 0