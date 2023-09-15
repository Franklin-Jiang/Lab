import cv2, copy, sys
import numpy as np
import matplotlib.pyplot as plt

# 将 NumPy 的默认截断改为系统允许的最大大小
np.set_printoptions(threshold=sys.maxsize)


def imshow(img, OpenCV=False):
    """展示图像"""
    # 如果展示的是 OpenCV 的图像
    if OpenCV:
        # 则要将 OpenCV 的 BGR 图像转换为 RGB 图像
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.axis("off")  # 去除坐标轴


def im_replace(img: np.array, _from, _to, not_equal=False):
    """_from 填诸如 [255,255,0]；_to 填诸如 [0,0,0]；not_equal 是不等条件，默认为 False 表等于条件，若为 True，则替换掉满足不等条件的元素"""
    # 获取深层拷贝
    img = copy.deepcopy(img)
    # 重塑数组的 shape
    shape = img.shape
    img_flatten = img.reshape((shape[0] * shape[1], shape[2]))
    # 进行替换
    if not_equal:
        # 如果是不相等的话，只要有一个元素不相等成立即可
        img_flatten[np.any(img_flatten != _from, axis=1)] = _to
    else:
        # 如果是相等的话，需要三个元素全都相等成立才行
        img_flatten[np.all(img_flatten == _from, axis=1)] = _to
    # 恢复数组的 shape
    img = img_flatten.reshape((shape[0], shape[1], shape[2]))
    # print(img_flatten)
    imshow(img)
    return img
