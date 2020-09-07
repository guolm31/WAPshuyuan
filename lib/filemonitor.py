#!/usr/bin/python
# coding=utf-8

import os


def FileMonitor(path_read):
    '''
    作用：监控目标文件夹并获取文件数量
    :param path_read: 监控文件夹路径
    :return: 文件数量
    '''
    # 存储获取到的文件
    file_names = []
    # 遍历文件夹
    file_list = os.walk(path_read)
    for a, b, c in file_list:
        for m in c:
            file_names.append(m)
    # 获取积压文件个数
    num = len(file_names)
    return num