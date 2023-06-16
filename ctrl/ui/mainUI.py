# python tk制作的界面

# 布局，大体上分为左右两个部分
# 高度暂定为720
# 左侧宽度暂定为320
# 右侧宽度暂定为960
# 左侧背景色粉色
# 右侧背景色白色

import tkinter as tk
from networkUI import NetworkUI
from cameraUI import CameraUI
from infoUI import InfoUI

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from ctrl.kInput import KInput

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
    infoUI = InfoUI(left_frame)
    infoUI.update_info("hello\nworld")

    cameraUI = CameraUI(right_frame,networkUI)

    kInput = KInput(networkUI,cameraUI)
    kInput.start()

    # 定义一个函数，用于在关闭窗口时调用两个 close 方法
    def on_closing():
        networkUI.close()
        cameraUI.close()
        root.destroy()

    # 为 root 窗口定义一个 protocol，当用户点击窗口的关闭按钮时，调用 on_closing 函数
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # 运行主循环
    root.mainloop()



if __name__ == '__main__':
    main()