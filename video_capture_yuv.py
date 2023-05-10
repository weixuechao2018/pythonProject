# encoding: utf-8

import cv2
import numpy as np


def uyvy2rgb(file_path, width, height, channels=3):
    # 读取文件
    img = np.fromfile(file_path, dtype=np.uint8)
    # Y, U, V 管道

    Y = np.zeros(height * width)
    U = np.zeros(height * width)
    V = np.zeros(height * width)
    index = 0

    # 按规律将数据填充进管道中
    while 8 * index < len(img):
        Y[4 * index] = img[8 * index + 1]
        Y[4 * index + 1] = img[8 * index + 3]
        Y[4 * index + 2] = img[8 * index + 5]
        Y[4 * index + 3] = img[8 * index + 7]

        U[4 * index] = img[8 * index]
        U[4 * index + 1] = img[8 * index]
        U[4 * index + 2] = img[8 * index + 4]
        U[4 * index + 3] = img[8 * index + 4]

        V[4 * index] = img[8 * index + 2]
        V[4 * index + 1] = img[8 * index + 2]
        V[4 * index + 2] = img[8 * index + 6]
        V[4 * index + 3] = img[8 * index + 6]
        index += 1

    # 转为RGB
    R = 1.164 * (Y - 16) + 2.018 * (U - 128)
    G = 1.164 * (Y - 16) - 0.813 * (V - 128) - 0.391 * (U - 128)
    B = 1.164 * (Y - 16) + 1.596 * (V - 128)

    rgb = np.zeros((height, width, channels))
    rgb[:, :, 0] = R.reshape((height, width))
    rgb[:, :, 1] = G.reshape((height, width))
    rgb[:, :, 2] = B.reshape((height, width))

    return rgb

def read_yuv422(image_path, rows, cols):
    """
    :param image_path: 待转换的.yuv图像文件路径
    :param rows: 图像行数
    :param cols: 图像列数
    :return: y,u,v分量
    """

    # 创建y分量
    img_y_1 = np.zeros((rows, int(cols/2)), np.uint8)
    img_y_2 = np.zeros((rows, int(cols / 2)), np.uint8)
    img_y = np.zeros((rows, cols), np.uint8)

    # 创建u分量
    img_u = np.zeros((rows, int(cols / 2)), np.uint8)

    # 创建v分量
    img_v = np.zeros((rows, int(cols / 2)), np.uint8)

    # 读取内存中数据
    with open(image_path, 'rb') as reader:
        for i in range(rows):
            for j in range(int(cols/2)):
                img_u[i, j] = ord(reader.read(1))
                img_y_1[i, j] = ord(reader.read(1))
                img_v[i, j] = ord(reader.read(1))
                img_y_2[i, j] = ord(reader.read(1))

    for i in range(rows):
        for j in range(int(cols/2)):
            img_y[i, 2*j] = img_y_1[i, j]
            img_y[i, 2*j+1] = img_y_2[i,j]

    return img_y, img_u, img_v

def yuv2rgb422(y, u, v):
    """
    :param y: y分量
    :param u: u分量
    :param v: v分量
    :return: rgb格式数据以及r,g,b分量
    """

    rows, cols = y.shape[:2]

    # 创建r,g,b分量
    r = np.zeros((rows, cols), np.uint8)
    g = np.zeros((rows, cols), np.uint8)
    b = np.zeros((rows, cols), np.uint8)

    for i in range(rows):
        for j in range(int(cols / 2)):
            r[i, 2 * j] = max(0, min(255, y[i, 2 * j] + 1.402 * (v[i, j] - 128)))
            g[i, 2 * j] = max(0, min(255, y[i, 2 * j] - 0.34414 * (u[i, j] - 128) - 0.71414 * (v[i, j] - 128)))
            b[i, 2 * j] = max(0, min(255, y[i, 2 * j] + 1.772 * (u[i, j] - 128)))

            r[i, 2 * j + 1] = max(0, min(255, y[i, 2 * j + 1] + 1.402 * (v[i, j] - 128)))
            g[i, 2 * j + 1] = max(0, min(255, y[i, 2 * j + 1] - 0.34414 * (u[i, j] - 128) - 0.71414 * (v[i, j] - 128)))
            b[i, 2 * j + 1] = max(0, min(255, y[i, 2 * j + 1] + 1.772 * (u[i, j] - 128)))

    rgb = cv2.merge([b, g, r])

    return rgb, r, g, b

class VideoCaptureYUV:
    def __init__(self, filename, size):
        self.height, self.width = size
        self.frame_len = self.width * self.height * 3 / 2
        self.f = open(filename, 'rb')
        self.shape = (int(self.height*1.5), self.width)

    def read_raw(self):
        try:
            raw = self.f.read(self.frame_len)
            yuv = np.frombuffer(raw, dtype=np.uint8)
            yuv = yuv.reshape(self.shape)
        except Exception as e:
            print(str(e))
            return False, None
        return True, yuv

    def read(self):
        ret, yuv = self.read_raw()
        if not ret:
            return ret, yuv
        bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_NV21)
        return ret, bgr
