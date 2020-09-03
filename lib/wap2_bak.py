#!/usr/local/bin/python
# coding:utf-8
# author:
# version:build 2020-08-25



import os

import  ftplib
from readconf import ReadConfig


def isFindTxt():
    cf = ReadConfig()
    # 设置监控路径
    path_log = cf.get('filepath','path_log')
    # 设置ftp ip
    ftp_ip = cf.get('ftp','ftp_ip')
    # 设置ftp 用户
    ftp_user = cf.get('ftp','ftp_user')
    # 设置ftp 密码
    ftp_passwd = cf.get('ftp','ftp_passwd')


    ftp = ftplib.FTP(ftp_ip)
    ftp.login(ftp_user, ftp_passwd)  # 登陆ftp服务器，连接的用户名，密码

    for parent, dirnames, filenames in os.walk(path_log):
        for filename in filenames:
            file_local = os.path.join(path_log,filename)
            # 设置FTP存储位置
            ftp_path = '/opt/patrol/{0}'.format(filename)
            bufsize = 1024
            fp = open(file_local, 'rb')
            ftp.storbinary('STOR ' + ftp_path, fp, bufsize)
            fp.close()
            os.remove(file_local)
    ftp.quit()  # 退出ftp服务器


if __name__ == '__main__':
    isFindTxt()

