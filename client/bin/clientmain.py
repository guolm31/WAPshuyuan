#!/usr/bin/python
# coding=utf-8

import sys
sys.path.append('../')
import time
from lib.filemonitor import FileMonitor
from lib.filecreat import FileCreat
from lib.readconfig import ReadConfig
from lib.fileerror import FileError
from lib.fileftp import FileFtp


cf = ReadConfig('config.ini')
# 获取主叫号码
org_phone = cf.get('phonenumber', 'org_phone')
# 获取被叫号码(存储成列表)
des_phones = cf.get('phonenumber', 'des_phone').split(',')

# 获取程序间隔时间
sleep_time = cf.getint('interval', 'sleeptime')

# 获取读取文件数目路径
path_read = cf.get('filepath', 'path_read')
# 获取通知日志存储路径
path_log = cf.get('filepath', 'path_log')
# 获取异常退信息存储路径
path_error = cf.get('filepath', 'path_error')

# 获取文件告警阈值
file_num = cf.getint('filenumber', 'filenum')

# 获取ftp ip
ftp_ip = cf.get('ftp','ftp_ip')
# 获取ftp 用户
ftp_user = cf.get('ftp','ftp_user')
# 获取ftp 密码
ftp_passwd = cf.get('ftp','ftp_passwd')
# 获取ftp 文件保存路径
ftp_path = cf.get('ftp','ftp_path')
# 获取本机ip
local_ip = cf.get('localip','local_ip')
# 获取本机平台
local_name = cf.get('localip','local_name')

if __name__ == '__main__':
    while True:
        try:
            #监控目标文件夹,获取文件数量
            num = FileMonitor(path_read)
            if num > file_num:
                # 生成通知文件
                FileCreat(org_phone,des_phones,path_log,num,local_ip,local_name)
                # 上传通知文件
                FileFtp(ftp_ip,ftp_user,ftp_passwd,ftp_path,path_log)
                # 休眠
                time.sleep(sleep_time)
        except Exception as e:
            # 生成异常文件，并保存错误日志
            FileError(e,path_error,des_phones,org_phone,path_log,local_ip)
            time.sleep(sleep_time)
