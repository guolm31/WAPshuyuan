#!/usr/bin/python
# coding=utf-8
import os
import datetime
import time
from readconf import ReadConfig
from fileftp import FileFtp

def file_monitor():
    try:
        # 存储获取到的文件
        file_names = []
        # 遍历文件夹
        file_list = os.walk(path_read)
        for a, b, c in file_list:
            for m in c:
                file_names.append(m)
        # 获取积压文件个数
        num = len(file_names)
        # 判断文件数，并处理
        if int(num) > file_num:
            # 获取文件执行时间
            time_now = datetime.datetime.now()
            # 设置告警信息
            error_text = '积压文件数量为{0}个'.format(num)
            # 设置日志文件名时间
            file_error = time_now.strftime('%Y%m%d%H%M%S')

            with open(r'{0}/{1}.txt'.format(path_log, file_error), 'w')as f:
                for des_phone in des_phones:
                    # 设置文本内容
                    text = "{0},{1},{2},{3}\n".format(time_now.strftime('%Y-%m-%d %H:%M:%S'), error_text, org_phone,
                                                      des_phone)
                    f.write(text)
            # 运行FTP程序
            FileFtp()

    except Exception as e:
        time_break = datetime.datetime.now()
        file_break = time_break.strftime('%Y%m%d%H%M%S')

        # 生成监控程序 退出告警
        with open(r'{0}/{1}.txt'.format(path_log, file_break), 'w')as f:
            for des_phone in des_phones:
                text_break = '{0},监控程序异常,{1},{2}\n'.format(time_break.strftime('%Y-%m-%d %H:%M:%S'), org_phone,
                                                             des_phone)
                f.write(text_break)
        # 存储异常信息
        with open(r'{0}/error.txt'.format(path_error), 'a')as f:
            error_time = time_break.strftime('%Y-%m-%d %H:%M:%S')
            f.write(error_time+'\t'+'告警内容：'+str(e)+'\n')




if __name__ == '__main__':
    cf = ReadConfig()
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
    while True:
        file_monitor()
        time.sleep(sleep_time)