#!/usr/local/bin/python
# coding:utf-8


import os
import ftplib


def CheckFtpClient(ftp_ip, ftp_user, ftp_passwd, checkftp_path_s, checkftp_path_c, local_ip):
    '''
    此方法用于上传ftp探测文件到目标服务器
     ftp_ip: 目标服务器IP
     ftp_user: ftp用户名
     ftp_passwd: ftp密码
     checkftp_path_s: 目标服务器存放路径
     checkftp_path_c: ftp探测文件保存路径
     local_ip:本机IP地址
    '''
    # 设置已本机IP命名的文件名
    filename = '{0}.txt'.format(local_ip)
    # 设置文件绝对路径
    file_local = os.path.join(checkftp_path_c, filename)

    #判断是否有文件，如果没有则创建
    files = os.listdir(checkftp_path_c)  # 得到文件夹下的所有文件名称,得到的是一个列表
    if filename not in files:
        with open(file_local,'w',encoding='utf-8')as f:
            pass


    ftp = ftplib.FTP(ftp_ip)
    ftp.login(ftp_user, ftp_passwd)  # 登陆ftp服务器，连接的用户名，密码

    # 设置FTP存储位置
    ftp_pathfile = '{0}/{1}'.format(checkftp_path_s, filename)
    bufsize = 1024
    fp = open(file_local, 'rb')
    ftp.storbinary('STOR ' + ftp_pathfile, fp, bufsize)
    fp.close()
    ftp.quit()  # 退出ftp服务器


if __name__ == '__main__':
    pass
