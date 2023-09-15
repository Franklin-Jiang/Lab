# %%
import cv2, copy, sys
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(threshold=sys.maxsize)


def imshow(img):
    """展示图像"""
    # cv2.imshow(caption, img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 将BGR图像转换为RGB图像
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 显示图像
    plt.imshow(img_rgb)
    plt.axis("off")  # 去除坐标轴



def im_replace(img: np.array, _from, _to, not_equal=False):
    """_from 填诸如 [255,255,0]；_to 填诸如 [0,0,0]；not_equal 是不等条件，默认为 False 表等于条件，若为 True，则替换掉满足不等条件的元素"""
    # 获取深层拷贝
    img = copy.deepcopy(img)
    # 获取数组的形状
    shape = img.shape
    img_flatten = img.reshape((shape[0] * shape[1], shape[2]))
    # 进行替换
    if not_equal:
        img_flatten[np.any(img_flatten != _from, axis=1)] = _to
    else:
        img_flatten[np.all(img_flatten == _from, axis=1)] = _to
    img = img_flatten.reshape((shape[0], shape[1], shape[2]))
    # print(img_flatten)
    imshow(img)
    return img


# 读取图像（第二个参数0表示以灰度图像方式读取图像）
img = cv2.imread("D:\\Codes\\VSCode_MATLAB\\Lab2\\counting_objects_rgb.png")
imshow(img)


# %%
img1 = im_replace(img, [255, 255, 0], [255, 255, 255])
img1 = im_replace(img1, [255, 255, 255], [0, 0, 0], not_equal=True)

# %%
# 获取深层拷贝
img = copy.deepcopy(img)
# 获取数组的形状
shape = img.shape
img_flatten = img.reshape((shape[0] * shape[1], shape[2]))
img_flatten[np.all(img_flatten == [255, 255, 0], axis=1)] = [255, 255, 255]
# img = img_flatten.reshape((shape[0], shape[1], shape[2]))
# print(img_flatten)
# imshow(img)

# %%
np.array([255,255,255]).shape

# %%
# # 将彩色图像转换为灰度图像
# gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # 对灰度图像进行阈值处理
# _, threshold_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# imshow(threshold_img)

# %%

# 二值化处理
_, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


# %%
class UnionFind:
    def __init__(self, element_num=None):
        self.parent = {}
        if element_num is not None:
            for i in range(element_num):
                self.add(i)

    def add(self, x):
        """工具函数"""
        # 如果已经存在则跳过
        if x in self.parent:
            return
        self.parent[x] = x

    def merge(self, x, y):
        if x not in self.parent:
            self.add(x)
        if y not in self.parent:
            self.add(y)
        # 查找到两个元素的树根
        x = self.find(x)
        y = self.find(y)
        # 如果相等，说明属于同一个集合
        if x == y:
            return
        elif x < y:
            self.parent[y] = x
        else:
            self.parent[x] = y

    def find(self, x):
        # 如果father[x] == x，说明x是树根
        if self.parent[x] == x:
            return x
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    # 判断是否属于同一个集合
    def same(self, x, y):
        return self.find(x) == self.find(y)


# %%

# %%
# 白色是 255，黑色是 0

np.count_nonzero(img == 0)

# %%
# %%
imshow(img)
ufs = UnionFind()
M, N = img.shape
I = np.zeros_like(img)

label = 1

# 如果左上角点为黑
if img[0, 0] == 0:
    I[0, 0] = label
    ufs.add(label)
    label += 1

for i in range(M):
    for j in range(N):
        # 如果该点为黑
        if img[i, j] == 0:
            # 如果是第一行
            if i == 0 and j != 0:
                # 取左元素的值
                val = I[i, j - 1]

                # 如果该值为标记值（非零值）
                if val != 0:
                    I[i, j] = val

                # 如果该值为零值
                else:
                    I[i, j] = label
                    ufs.add(label)
                    label += 1

            # 如果是第一列
            elif i != 0 and j == 0:
                # 取上元素的值
                val = I[i - 1, j]

                # 如果该值为标记值（非零值）
                if val != 0:
                    I[i, j] = val

                # 如果该值为零值
                else:
                    I[i, j] = label
                    ufs.add(label)
                    label += 1

            # 对于中间的常规元素
            else:
                # 取左元素和上元素的值
                a = I[i, j - 1]
                b = I[i - 1, j]

                I[i, j] = a or b
                if I[i, j] == 0:
                    I[i, j] = label
                    ufs.add(label)
                    label += 1

                if a and b:
                    ufs.merge(a, b)

for i in range(M):
    for j in range(N):
        # 如果该点为黑
        if img[i, j] == 0:
            # print(I[i, j], ufs.find(I[i, j]))
            I[i, j] = ufs.find(I[i, j])

# %%
len(set(ufs.parent.values()))


# %% Test
