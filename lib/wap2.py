#!/usr/local/bin/python
# coding:utf-8
# author:
# version:build 2020-08-25


import time
import os
from ftplib import FTP  #加载ftp模块
import zipfile, ftplib

path = input('请输入文件目录路径')  #定期扫描日志目录中的文件r"C:\Users\Administrator\Desktop\log"

def isFindTxt(path):  # 查找指定目录，判断是否有文件，有的话，return table
    while 1:
        if not os.listdir(path):
            print('日志目录没有文件,继续定期扫描')
            time.sleep(60 * 60)
        else:
            print('日志目录有文件,将文件ftp到服务器并备份到备份目录')

            t = time.strftime('%Y-%m-%d', time.localtime(time.time()))     #接收时间元组，并返回以可读字符串表示的当地时间
            ftp = ftplib.FTP("ftp服务器IP")
            ftp.login("用户名", "密码")  # 登陆ftp服务器，连接的用户名，密码

            def make_zip(source_dir, output_filename):  # 定义压缩函数，
            zipf = zipfile.ZipFile(output_filename, 'w')
            pre_len = len(os.path.dirname(source_dir))
            for parent, dirnames, filenames in os.walk(source_dir):

                for filename in filenames:
                    pathfile = os.path.join(parent, filename)
                    arcname = pathfile[pre_len:].strip(os.path.sep)
                    zipf.write(pathfile, arcname)
            zipf.close()

            make_zip('文件URL地址', "%s.zip" % t)  # 将文件打包成 年-月-日.zip

            def ftp_upload():  # 定义上传函数
            file_remote = '%s.zip' % t
            file_local = './%s.zip' % t
            bufsize = 1024
            fp = open(file_local, 'rb')
            ftp.storbinary('STOR ' + file_remote, fp, bufsize)
            fp.close()
            ftp_upload()  # 将文件上传至服务器
            ftp.quit()  # 退出ftp服务器
            exit()  # 代码结束

    time.sleep(60 * 60)

