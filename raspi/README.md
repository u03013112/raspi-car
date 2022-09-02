# 这部分代码将在raspi上运行

## 放到docker里是为了方便部署

## 获得raspi ip的方法：
树莓派连接到相同局域网后，总是需要定位他的IP，这个很麻烦
用ddns的方式还需要一个有效的域名，另外就是更新不够及时
偶然间在网上找到一个有趣的帖子，好像树莓派默认支持的协议里有类似NetBIOS的主机名查询功能，所以这个会比较方便。就算不能有效的映射主机名，也可以通过硬记住自己pi的mac来进行ip定位
并将pi 的 ip 写到脚本里
### 以下是方案，带回家后验证没问题讲写到同步脚本中
环境：电脑和树莓派链接在同一网络内；
arp-scan工具能扫出局域网所有的IP地址；
安装arp-scan：
mac os
brew install arp-scan
Ubuntu
`注意：这个玩意需要root权限，需要sudo`
扫描以太网IP地址：
sudo arp-scan --interface en0 --localnet 
简写
sudo arp-scan --I en0 --l

## 新的有刷电调的坑
之前用的l298n来做的动力控制，主要问题是电流不足。想要电机有足够的电流，选择了支持电流更大的eagle 30A有刷电调。采用PWM来控制。
其中得到结论：虽然说明书的上说该电调支持的频率是2KHz，但实际使用时发现50Hz仍旧可以驱动。在刹车开启的前提下，`4%的占空比是油门初始状态，低于4%的占空比电调认为没有油门信号并报警`，`在提供超过4%的占空比一段时间，大概3秒之后，电调才进入就绪状态`，如果没有进入就绪状态，给出合理的占空比他也不会有任何电压输出。上限的占空比大致在12%，超过12%会失去动力。

下面是我在网上查到别人写的帖子，没有找到佐证，比如文中提到的航模标准，但是由于前面写的内容与我自己测试结果吻合度高，所以认为可信：
单片机输出1ms~2ms的方波脉冲，根据航模标准，PWM信号线的频率应该是50Hz，对应的每个周期总时长是20ms，输出到电调的油门线（控制线，也就是细细的，除了红的是接5V电源，黑的GND，另外那个就是数据线）。
如果是单向电调，1ms表示0%的油门，2ms表示100%的油门。如果是双向电调（有正、反转和刹车），标准1.5ms是0点，1ms是反向油门最大（100%油门），用于刹车或反转；2ms正向油门最大（100%油门），用于正转。
这是无线遥控模型比例控制的一个标准。对于其它电调也一样。注意，电调转速只与1ms~2ms的脉宽有关，与脉冲重复率无关。1~2ms的方波脉宽渐变过程对应油门的从小到大，从负到正的渐变。 脉宽的幅度2.5V~6V；所以3~5V工作电压的单片机都适用。