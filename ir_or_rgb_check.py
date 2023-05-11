# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import sys
import shutil
import time

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageStat

from file_hepler import *
from video_capture_yuv import *

# 方式一
def image_show_gray(image):
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    r, g, b = cv2.split(image)

    r = r.astype(np.float32)
    g = g.astype(np.float32)
    b = b.astype(np.float32)

    s_w, s_h = r.shape[:2]

    x = (r + b + g) / 3

    r_gray = abs(r - x)
    g_gray = abs(g - x)
    b_gray = abs(b - x)

    area = s_w * s_h
    r_sum = np.sum(r_gray) / area
    g_sum = np.sum(g_gray) / area
    b_sum = np.sum(b_gray) / area

    gray_degree = (r_sum + g_sum + b_sum) / 3

    if gray_degree < 10:
        # print("Gray")
        return True
    else:
        print("NOT Gray")
        return False

def gray_check(image):
    sp = image.shape
    height = sp[0]  # height(rows) of image
    width = sp[1]  # width(colums) of image

    target_size = (width, height)
    grid_num = 40
    grid_width = int(target_size[0] / grid_num)
    grid_height = int(target_size[1] / grid_num)

    for i in range(grid_num):
        interval_h_start = i * grid_height
        interval_h_end = (i + 1) * grid_height
        for j in range(grid_num):
            interval_w_start = j * grid_width
            interval_w_end = (j + 1) * grid_width
            check_img = image[interval_h_start: interval_h_end, interval_w_start: interval_w_end]
            if image_show_gray(check_img) == False:
                return False

    return True

# 方式二
def gray_check2(img, threshold = 15):
    """
    入参：
    img：PIL读入的图像
    threshold：判断阈值，图片3个通道间差的方差均值小于阈值则判断为灰度图。
    阈值设置的越小，容忍出现彩色面积越小；设置的越大，那么就可以容忍出现一定面积的彩色，例如微博截图。
    如果阈值设置的过小，某些灰度图片会被漏检，这是因为某些黑白照片存在偏色，例如发黄的黑白老照片、
    噪声干扰导致灰度图不同通道间值出现偏差（理论上真正的灰度图是RGB三个通道的值完全相等或者只有一个通道，
    然而实际上各通道间像素值略微有偏差看起来仍是灰度图）
    出参：
    bool值
    """
    sp = img.shape
    width = sp[0]  # height(rows) of image
    height = sp[1]  # width(colums) of image

    # target_size = (int(height/20), int(width/20))
    target_size = (int(width / 20), int(height / 20))
    img = cv2.resize(img, dsize=target_size, interpolation=cv2.INTER_AREA)

    [aisle_b, aisle_g, aisle_r] = cv2.split(img)

    r = np.asarray(aisle_r, dtype=np.float32)
    g = np.asarray(aisle_g, dtype=np.float32)
    b = np.asarray(aisle_b, dtype=np.float32)

    r_value = cv2.Laplacian(aisle_r, cv2.CV_64F).var()
    g_value = cv2.Laplacian(aisle_g, cv2.CV_64F).var()
    b_value = cv2.Laplacian(aisle_b, cv2.CV_64F).var()


    diff1 = np.var(r - g)
    diff2 = (g - b).var()
    diff3 = (b - r).var()

    diff_sum = (diff1 + diff2 + diff3) / 3.0
    print("diff_sum:" + str(diff_sum))
    if diff_sum <= threshold:
        return True
    else:
        return False

# 方式三 不可靠
def gray_check3(chip):
    img_hsv = cv2.cvtColor(chip, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(img_hsv)
    s_w, s_h = s.shape[:2]

    h_sum = np.sum(h) / (s_w * s_h)
    s_sum = np.sum(s) / (s_w * s_h)
    v_sum = np.sum(v) / (s_w * s_h)

    if s_sum > 10:
        return False
    return True

def color_or_gray(file_path):
    im = Image.open(file_path).convert("RGB")
    stat = ImageStat.Stat(im)
    if sum(stat.sum) / 3 == stat.sum[0]:
        # return('gray')
        return True
    else:
        # return('color')
        return False

def gray_check5(image):
    # [aisle_b, aisle_g, aisle_r] = cv2.split(img)
    # sum_b = np.sum(aisle_b)
    # sum_g = np.sum(aisle_g)
    # sum_r = np.sum(aisle_r)

    hist = cv2.calcHist([image], [0], None, [256], [0, 256])

    hist_size = 256
    hist_range = (0, hist_size)
    r_hist = cv2.calcHist([image], [0], None, [hist_size], hist_range)
    g_hist = cv2.calcHist([image], [1], None, [hist_size], hist_range)
    b_hist = cv2.calcHist([image], [2], None, [hist_size], hist_range)

    # r_sum = np.average(r_hist)
    # g_sum = np.average(g_hist)
    # b_sum = np.average(b_hist)
    #
    # r_mean = np.mean(r_hist)
    # g_mean = np.mean(g_hist)
    # b_mean = np.mean(b_hist)

    xxx = np.mean(hist[60:90])
    xxxx = np.mean(hist[150:180])
    if np.max(hist[60:90]) > np.max(hist[150:180]):
        print("这可能是一个RGB图像。")
        return False
    else:
        print("这可能是一个红外图像。")
        return True

# 不可用
def gray_check4(img):
    if len(img.shape) == 3 and img.shape[2] == 3:
        # print("For RGB image: 3 channels")
        gray_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        if gray_img is None:
            return True
        return False
    else:
        img_gray = img  # For IR image: single channel
        print("For IR image: single channel")

def folder_image_check_variance(path ,suffix, type):
    folder_list_result = search_current_sameSuffix_file(path, suffix, False)
    print(len(folder_list_result))
    count = 0
    count_gray = 0
    size = (1920, 1280)
    for index in folder_list_result:
        print("start file path:" + index)
        if type == 1:
            img = cv2.imread(index)
        elif type == 2:
            img = uyvy2rgb(index, 1920, 1280, 3)
            # ret, img = cap.read()
        else:
            print("invalid")
            continue

        current_time_start = int(time.time())
        # if gray_check(img) == True:
        if gray_check2(img) == True:
        # if gray_check3(img) == True:
        # if gray_check4(img) == True:
        # if gray_check5(img) == True:
            count_gray += 1
            print(index + " is gray; count_gray = " + str(count_gray))
            current_time_stop = int(time.time())
            # print(current_time_stop - current_time_start)
        count += 1
        print("end file path:" + index + " ; count = " + str(count))

if __name__ == '__main__':
    # imgs = cv2.imread("/home/weixuechao/Downloads/1/85701999360015.png")
    # imgs = cv2.imread("/home/weixuechao/Downloads/15_1/15121865458175.png")
    # imgs = cv2.imread("/home/weixuechao/Downloads/15_1/1235.jpg")
    # imgs = cv2.imread("/home/weixuechao/Downloads/15_1/32848588716562.png")
    # imgs = cv2.imread("/home/weixuechao/Downloads/15_1/15164467154964.png")
    imgs = cv2.imread("/home/weixuechao/Downloads/15_1/0001.jpg")
    # image_show_gray(imgs)
    # gray_check(imgs)
    gray_check2(imgs)
    gray_check3(imgs)
    gray_check5(imgs)

    folder_image_path = "/home/weixuechao/Downloads/jidu-img"
    folder_image_check_variance(folder_image_path, "jpg", 1)
    # folder_image_check_variance(folder_image_path, "png", 1)
    # folder_image_check_variance("/home/weixuechao/Downloads/11", "uyvy", 2)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
