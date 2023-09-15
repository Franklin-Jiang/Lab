# %%
from tool import *

# 读取图像（第二个参数0表示以灰度图像方式读取图像）
img = imread("1_counting_objects_rgb.png")

# %% 将彩图转化为 BW 图
img = im_replace(img, (0, 255, 255), (255, 255, 255))
img = im_replace(img, (255, 255, 255), (0, 0, 0), not_equal=True)

# %%
# 初始化并查集
ufs = UnionFind()
# 将三通道 BGR 转成单通道
img = img[:, :, 0]
# 获取图像的尺寸
M, N = img.shape
I = np.zeros_like(img, dtype=np.int32)

label = 1

# 如果左上角点为黑
if img[0, 0] == 0:
    I[0, 0] = label
    ufs.add(label)
    label += 1

# 第一遍
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

# 第二遍
for i in range(M):
    for j in range(N):
        # 如果该点为黑
        if img[i, j] == 0:
            # print(I[i, j], ufs.find(I[i, j]))
            I[i, j] = ufs.find(I[i, j])

print("Number of objects:", len(set(ufs.parent.values())))
