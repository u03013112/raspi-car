# 代码从
# https://github.com/fuenwang/Equirec2Perspec 
# 复制而来，稍作修改
# 将之前的水平视角与垂直视角相同，改为可以分别设置

import os
import sys
import cv2
import numpy as np

def xyz2lonlat(xyz):
    # 降低精度，加快运算速度
    xyz = xyz.astype(np.float32)

    atan2 = np.arctan2
    asin = np.arcsin

    norm = np.linalg.norm(xyz, axis=-1, keepdims=True)
    xyz_norm = xyz / norm
    x = xyz_norm[..., 0:1]
    y = xyz_norm[..., 1:2]
    z = xyz_norm[..., 2:]

    lon = atan2(x, z)
    lat = asin(y)
    lst = [lon, lat]

    out = np.concatenate(lst, axis=-1)
    return out
import timeit
def lonlat2XY(lonlat, shape):
    X = (lonlat[..., 0:1] / (2 * np.pi) + 0.5) * (shape[1] - 1)
    Y = (lonlat[..., 1:] / (np.pi) + 0.5) * (shape[0] - 1)
    
    lst = [X, Y]
    out = np.concatenate(lst, axis=-1)
    return out 

class Equirectangular:
    def __init__(self, img):
        self._img = img
        [self._height, self._width, _] = self._img.shape

    def GetPerspective(self, FOV_horizontal, FOV_vertical, THETA, PHI, height, width):
        f_horizontal = 0.5 * width * 1 / np.tan(0.5 * FOV_horizontal / 180.0 * np.pi)
        f_vertical = 0.5 * height * 1 / np.tan(0.5 * FOV_vertical / 180.0 * np.pi)
        cx = (width - 1) / 2.0
        cy = (height - 1) / 2.0
        K = np.array([
                [f_horizontal, 0, cx],
                [0, f_vertical, cy],
                [0, 0,  1],
            ], np.float32)
        K_inv = np.linalg.inv(K)

        # ...（其余代码不变）

        x = np.arange(width)
        y = np.arange(height)
        x, y = np.meshgrid(x, y)
        z = np.ones_like(x)
        xyz = np.concatenate([x[..., None], y[..., None], z[..., None]], axis=-1)
        xyz = xyz @ K_inv.T
        
        y_axis = np.array([0.0, 1.0, 0.0], np.float32)
        x_axis = np.array([1.0, 0.0, 0.0], np.float32)
        R1, _ = cv2.Rodrigues(y_axis * np.radians(THETA))
        R2, _ = cv2.Rodrigues(np.dot(R1, x_axis) * np.radians(PHI))
        R = R2 @ R1
        xyz = xyz @ R.T
        
        lonlat = xyz2lonlat(xyz) 
        
        XY = lonlat2XY(lonlat, shape=self._img.shape)
        # .astype(np.float32)
        # persp = cv2.remap(self._img, XY[..., 0], XY[..., 1], cv2.INTER_CUBIC, borderMode=cv2.BORDER_WRAP)
        persp = cv2.remap(self._img, XY[..., 0], XY[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
        # elapsed_time = timeit.default_timer() - start_time
        # print(f"Execution time: {elapsed_time * 1000:.2f} ms")
        return persp