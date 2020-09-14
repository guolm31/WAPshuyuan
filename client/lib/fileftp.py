#!/usr/local/bin/python
# coding:utf-8
# author:
# version:build 2020-08-25

import os
import  ftplib
from lib.readconf import ReadConfig


def FileFtp(ftp_ip,ftp_user,ftp_passwd,ftp_path,path_log):
    '''
    此模块用于上传文件到目标服务器
    :param ftp_ip: 目标服务器IP
    :param ftp_user: ftp用户名
    :param ftp_passwd: ftp密码
    :param ftp_path: 目标服务器存放路径
    :param path_log: 本地文件保存路径
    '''
    ftp = ftplib.FTP(ftp_ip)
    ftp.login(ftp_user, ftp_passwd)  # 登陆ftp服务器，连接的用户名，密码

    for parent, dirnames, filenames in os.walk(path_log):
        for filename in filenames:
            file_local = os.path.join(path_log,filename)
            # 设置FTP存储位置
            ftp_pathfile = '{0}/{1}'.format(ftp_path,filename)
            bufsize = 1024
            fp = open(file_local, 'rb')
            ftp.storbinary('STOR ' + ftp_pathfile, fp, bufsize)
            fp.close()
            os.remove(file_local)
    ftp.quit()  # 退出ftp服务器


if __name__ == '__main__':
    cf = ReadConfig()
    # 设置监控 路径
    path_log = cf.get('filepath','path_log')
    # 设置ftp ip
    ftp_ip = cf.get('ftp','ftp_ip')
    # 设置ftp 用户
    ftp_user = cf.get('ftp','ftp_user')
    # 设置ftp 密码
    ftp_passwd = cf.get('ftp','ftp_passwd')
    # 设置ftp 文件保存路径
    ftp_path = cf.get('ftp','ftp_path')
    FileFtp(ftp_ip,ftp_user,ftp_passwd,ftp_path,path_log)

