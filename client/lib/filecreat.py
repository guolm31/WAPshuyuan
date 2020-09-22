#!/usr/bin/python
# coding=utf-8


import datetime
import time
##from lib.readconf import ReadConfig

def FileCreat(org_phone,des_phones,path_log,num,localip,localname,path_read):
    '''
    此模块用于生成通知文件
    :param org_phone: 通知短信主叫号码
    :param des_phones: 通知短信被叫号码
    :param path_log: 通知文件存储路径
    :param num: 监控文件数量
    :param localip:本机ip
    '''
    # 获取文件执行时间
    time_now = datetime.datetime.now()
    # 设置告警信息
    error_text = '积压文件数量为{0}个'.format(num)
    # 设置日志文件名时间
    file_error = time_now.strftime('%Y%m%d%H%M%S')

    with open(r'{0}/{1}.txt'.format(path_log, file_error), 'w',encoding='utf-8')as f:
        for des_phone in des_phones:
            # 设置文本内容
            text = "{0},{1},{2},{3},{4},{5},{6}\n".format(time_now.strftime('%Y-%m-%d %H:%M:%S'), error_text, org_phone,
                                              des_phone,localip,localname,path_read)
            f.write(text)

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
    # 设置ftp ip
    ftp_ip = cf.get('ftp','ftp_ip')
    # 设置ftp 用户
    ftp_user = cf.get('ftp','ftp_user')
    # 设置ftp 密码
    ftp_passwd = cf.get('ftp','ftp_passwd')
    # 设置ftp 文件保存路径
    ftp_path = cf.get('ftp','ftp_path')
    #while True:
       # file_monitor()
        #time.sleep(sleep_time)