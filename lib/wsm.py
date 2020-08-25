#!/usr/local/bin/python
# coding:utf-8

import time
import os

path = input('请输入文件目录路径')  # 让用户自行输入路径
r"C:\Users\王少敏\Desktop\python实践\log"

def isFindTxt(path):  # 查找指定目录，判断是否有文件，有的话，return table
    while 1:
        if not os.listdir(path):
            print('未收到告警文件,继续定期扫描')
            time.sleep(60 * 60)
        else:
            message_table = []
            print('收到告警文件,将读取文件并清空文件夹')
        files = os.listdir(path)  # 得到文件夹下的所有文件名称,得到的是一个列表
        for file in files:
            if not os.path.isdir(file):
                with open(path + '/' + file, 'r', encoding='gbk') as f:
                    iter_f = iter(f)
                    str = ""
                    for line in iter_f:
                        str = str + line
                    str1 = str.split(',')
    message_table.append(str1)
    if len(message_table) != 0:
        sendmessage()  # 调用发送短信函数
    removeTxt(path)
    time.sleep(60 * 60)
    return


def removeTxt(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

print(isFindTxt(path))