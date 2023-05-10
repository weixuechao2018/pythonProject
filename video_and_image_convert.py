import cv2
import shutil
import os

import file_hepler
from file_hepler import *

# capture.set(CV_CAP_PROP_FRAME_WIDTH, 1080);# 宽度
# capture.set(CV_CAP_PROP_FRAME_HEIGHT, 960);# 高度
# capture.set(CV_CAP_PROP_FPS, 30);# 帧率 帧/秒
# capture.set(CV_CAP_PROP_BRIGHTNESS, 1);# 亮度 1
# capture.set(CV_CAP_PROP_CONTRAST,40);# 对比度 40
# capture.set(CV_CAP_PROP_SATURATION, 50);# 饱和度 50
# capture.set(CV_CAP_PROP_HUE, 50);# 色调 50
# capture.set(CV_CAP_PROP_EXPOSURE, 50);# 曝光 50

# 获取摄像头参数
# capture.get(CV_CAP_PROP_FRAME_WIDTH);
# capture.get(CV_CAP_PROP_FRAME_HEIGHT);
# capture.get(CV_CAP_PROP_BRIGHTNESS);
# capture.get(CV_CAP_PROP_CONTRAST);
# capture.get(CV_CAP_PROP_SATURATION);
# capture.get(CV_CAP_PROP_HUE);
# capture.get(CV_CAP_PROP_EXPOSURE); # 获取视频参数：
# 获取视频参数
# capture.get(CV_CAP_PROP_FRAME_COUNT);# 视频帧数
# 帧率 帧/秒
# capture.get(CV_CAP_PROP_FPS);

def video2images(video_file, image_format="jpg", img_path="", frames_rate=20, all_convert=True):
    if img_path == "":
        index = int(video_file.rindex('.'))
        img_path = video_file[0:index]

    # 文件检查
    if not os.path.exists(img_path):
        os.makedirs(img_path)             # 目标文件夹不存在，则创建
    else:
        shutil.rmtree(img_path)
        os.makedirs(img_path)

    cap = cv2.VideoCapture(video_file)    # 获取视频
    judge = cap.isOpened()                 # 判断是否能打开成功
    print(judge)

    # 视频信息
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))      # 帧率，视频每秒展示多少张图片
    print('fps:', fps)
    duration = length / fps
    print(f"{video_file}: {duration} seconds")

    if all_convert == False:
        length_num = len(str(int(length / frames_rate)))
    else:
        length_num = len(str(length))

    frames = 1                           # 用于统计所有帧数
    count = 1                            # 用于统计保存的图片数量

    if image_format == "jpg":
        image_gname = ".jpg"
        frame_params = [cv2.IMWRITE_JPEG_QUALITY, 100]
    elif image_format == "png":
        image_gname = ".png"
        frame_params = [cv2.IMWRITE_PNG_COMPRESSION, 10]
    elif image_format == "jpeg":
        image_gname = ".jpeg"
        frame_params = [cv2.IMWRITE_JPEG_QUALITY, 100]
    # elif image_format == "tiff":
    #     image_gname = str(count).rjust(4, '0') + ".tiff"
    #     frame_params = [cv2.IMWRITE_JPEG_QUALITY, 100]
    else:
        print("")
        return False

    while(judge):
        flag, frame = cap.read()         # 读取每一张图片 flag表示是否读取成功，frame是图片
        if not flag:
            print(flag)
            print("Process finished!")
            break
        else:
            # 每隔frames_rate帧抽一张
            per_frame_write = False
            if all_convert == True:
                per_frame_write = True
            elif all_convert == False and frames % frames_rate == 0:
                per_frame_write = True
            else:
                per_frame_write = False

            if per_frame_write == True:
                name = str(count).rjust(length_num, '0') + image_gname
                # new_path = img_path + image_gname
                new_path = os.path.join(img_path, name)
                print(new_path)
                cv2.imwrite(new_path, frame, frame_params)
                # cv2.imencode('.jpg', frame)[1].tofile(newPath)
                count += 1

        frames += 1
    cap.release()
    print("共有 %d 张图片"%(count-1))
    return True

# def file_dir(video_path):
#     files = os.listdir(video_path)
#     os.chdir(video_path)
#     print("【注意】路径已经更换：%s" % os.getcwd())
#     # os.path.isfile()判断是否为文件，如果是返回值为True
#     # os.path.isdir()判断是否为目录(文件夹)，如果是返回值为True
#     for i in files:
#         if os.path.isfile(i):
#             file_list.append(i)
#         else:
#             dir_list.append(i)

def video2image_list(video_path, image_format="jpg", img_path="", frames_rate=20, all_convert=True):
    for dir in video_path:
        # print("共有 %s 张图片"(dir))
        video2images(dir, image_format, img_path, frames_rate, all_convert)


# 转MP4
# def create_mp4(filename, fps, images):
#   h, w, c = images[0].shape
#   fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#   writer = cv2.VideoWriter(filename, fourcc, fps, (w, h))
#   for frame in images:
#     writer.write(frame)
#   writer.release()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    all_files = []
    # folder_list("/home/weixuechao/Downloads", all_files)
    # folder_list_result = search_current_sameSuffix_file("/home/weixuechao/Downloads", "mp4", False)
    # folder_list_result = folder_same_suffix_list("/home/weixuechao/Downloads", ".mp4", False)
    # video2image_list(folder_list_result, "jpg", "", 20, False)
    video2images("/home/weixuechao/Downloads/DCD-55524/dump_20230505100521_15_1.mp4")
