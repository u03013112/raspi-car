# python tk制作的界面

# 布局，大体上分为左右两个部分
# 高度暂定为720
# 左侧宽度暂定为320
# 右侧宽度暂定为960
# 左侧背景色粉色
# 右侧背景色白色

import tkinter as tk
from networkUI import NetworkUI

def main():
    # 创建主窗口
    root = tk.Tk()
    root.geometry("1280x720")  # 设置窗口大小
    root.title("raspi car")
    root.configure(bg="pink")  # 设置root窗口的背景色

    # 创建左侧框架
    left_frame = tk.Frame(root, width=320, height=720, bg="pink")
    left_frame.pack(side="left", fill="both", anchor='nw')



    # 创建右侧框架
    right_frame = tk.Frame(root, width=960, height=720, bg="white")
    right_frame.pack(side="right", fill="both")

    networkUI = NetworkUI(left_frame)

    # 运行主循环
    root.mainloop()



if __name__ == '__main__':
    main()