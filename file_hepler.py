import os

# 子函数，显示所有文件的路径
def folder_list(path):
    all_files = []
    # 显示当前目录所有文件和子文件夹，放入file_list数组里
    file_list = os.listdir(path)
    # 循环判断每个file_list里的元素是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量
        cur_path = os.path.join(path, file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            # 递归
            all_files += folder_list(cur_path)
        else:
            # 将file添加进all_files里
            all_files.append(cur_path)

    return all_files

def folder_same_suffix_list(path, file_suffix, current_path):
    file_result = []
    # 显示当前目录所有文件和子文件夹，放入file_list数组里
    file_list = os.listdir(path)
    # 循环判断每个file_list里的元素是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量
        cur_path = os.path.join(path, file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            if current_path == True:
                continue
            # 递归
            file_result += folder_same_suffix_list(cur_path, file_suffix, current_path)
        else:
            # 将file添加进all_files里
            if file.endswith(file_suffix):
                file_result.append(cur_path)

    return file_result

# 查找该层文件夹下所有的文件及文件夹，返回列表
def search_all_path_file(dirPath, current_path=True):
    file_result = []
    dirs = os.listdir(dirPath)
    for currentFile in dirs:
        file_name = dirPath + '/' + currentFile
        # 如果是目录则递归，继续查找该目录下的文件
        if os.path.isdir(file_name):
            if current_path == False:
                search_all_path_file(file_name, current_path)
            else:
                continue
        else:
            file_result.append(file_name)

    return file_result

# 只能搜索.txt .avi 等后缀带.xxx的文件
def search_current_sameSuffix_file(dir_path, suffix, current_path=True):
    file_result = []
    dirs = os.listdir(dir_path)
    for currentFile in dirs:
        file_name = dir_path + '/' + currentFile
        if os.path.isdir(file_name):
            if current_path == False:
                search_current_sameSuffix_file(file_name, suffix, current_path)
            else:
                continue
        elif currentFile.split('.')[-1] == suffix:
            file_result.append(file_name)

    return file_result


# def folder_list(root_dir, file_suffix, current_path=True):
#     file_result = []
#     for dir in os.listdir(root_dir):
#         child = os.path.join(root_dir, dir)
#
#         if child.endswith(file_suffix) and os.path.isfile(child):
#             file_result.append(child)
#         else:
#             folder_list(child, file_suffix, current_path)
#
#         # for i in files:
#         #     if os.path.isfile(i):
#         #         file_list.append(i)
#         #     else:
#         #         dir_list.append(i)
#         # if os.path.isdir(child):
#         #     if current_path == True:
#         #         continue
#         #     folder_list(child, file_suffix, current_path)
#         #     for f1 in os.listdir(child):
#         #         if f1.endswith(file_suffix) and os.path.isfile(f1):
#         #             file_result.append(f1)
#
#     print(file_result)
#     return file_result