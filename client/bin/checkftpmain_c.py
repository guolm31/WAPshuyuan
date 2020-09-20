#!/usr/bin/python
# coding=utf-8

import time
import sys
sys.path.append('../')
import os
from lib.readconfig import ReadConfig
from lib.checkftp_c import CheckFtpClient


cf = ReadConfig('config.ini')

# 获取ftp ip
ftp_ip = cf.get('ftp','ftp_ip')
# 获取ftp 用户
ftp_user = cf.get('ftp','ftp_user')
# 获取ftp 密码
ftp_passwd = cf.get('ftp','ftp_passwd')

# 获取本机ip
local_ip = cf.get('localip','local_ip')

# 获取本机ftp探测文件存储路径
checkftp_path_c = os.path.join(os.path.abspath('..'),'log', 'checkftppath')
# 获取服务端探测FTP存储路径
checkftp_path_s = cf.get('checkftp','checkftp_path_s')
# 获取探测休眠时间
checksleep = cf.getint('checkftp','check_sleep')

if __name__ == '__main__':
    while True:
        try:
            CheckFtpClient(ftp_ip,ftp_user,ftp_passwd,checkftp_path_s,checkftp_path_c,local_ip)
            time.sleep(checksleep)

        except Exception as e:
            print(e)
            time.sleep(checksleep)