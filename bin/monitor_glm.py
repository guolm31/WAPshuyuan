#!/usr/bin/python
# coding=utf-8
#edit by guolm 2020-09-08

import sys
sys.path.append('../')
import time
from lib.filemonitor import FileMonitor
from lib.filecreat import FileCreat
from lib.readconfig import ReadConfig
from lib.fileerror import FileError
from lib.fileftp import FileFtp
import lib.logger as logger
import logging

cf = ReadConfig('config_client.ini')
# 设置主叫号码
org_phone = cf.get('phonenumber', 'org_phone')
# 设置被叫号码(存储成列表)
des_phones = cf.get('phonenumber', 'des_phone').split(',')
# 设置读取文件数目路径
path_read = cf.get('filepath', 'path_read')
# 设置通知日志存储路径
path_log = cf.get('filepath', 'path_log')
# 设置异常退信息存储路径
path_error = cf.get('filepath', 'path_error')
# 设置程序间隔时间
sleep_time = cf.getint('interval', 'sleeptime')
# 设置文件告警阈值
file_num = cf.getint('filenumber', 'filenum')
# 设置ftp ip
ftp_ip = cf.get('ftp','ftp_ip')
# 设置ftp 用户
ftp_user = cf.get('ftp','ftp_user')
# 设置ftp 密码
ftp_passwd = cf.get('ftp','ftp_passwd')
# 设置ftp 文件保存路径
ftp_path = cf.get('ftp','ftp_path')

if __name__ == '__main__':
    mylogger=logger.Logger()
    logging.error('this is a error from monitor_glm.py')
    while True:
        try:
            #监控目标文件夹,获取文件数量
            num = FileMonitor(path_read)
            if num > file_num:
                # 生成通知文件
                FileCreat(org_phone,des_phones,path_log,num)
                # 上传通知文件
                FileFtp(ftp_ip,ftp_user,ftp_passwd,ftp_path,path_log)
                logging.error("ftp file success")
                # 休眠
        except Exception as e:
            # 生成异常文件，并保存错误日志
            FileError(e,path_error,des_phones,org_phone,path_log)
        time.sleep(sleep_time)
