#!/usr/bin/python
# coding=utf-8

import datetime
#from lib.readconf import ReadConfig

def FileError(e,path_error,des_phones,org_phone,path_log,localip):
    '''
    此方法用于报错的处理
    :param e: 报错的内容
    :param path_error: 报错的存储路径
    :param des_phones: 通知短信的被叫号码
    :param path_log: 需要ftp的文件路径
    :param localip:本机ip
    '''
    time_break = datetime.datetime.now()
    file_break = time_break.strftime('%Y%m%d%H%M%S')

    # 生成监控程序 退出告警
    with open(r'{0}/{1}.txt'.format(path_log, file_break), 'w')as f:
        for des_phone in des_phones:
            text_break = '{0},{1}监控程序异常,{2},{3}\n'.format(time_break.strftime('%Y-%m-%d %H:%M:%S'),localip, org_phone,
                                                       des_phone)
            f.write(text_break)
    # 存储异常信息
    with open(r'{0}/error.txt'.format(path_error), 'a')as f:
        error_time = time_break.strftime('%Y-%m-%d %H:%M:%S')
        f.write(error_time + '\t' + '告警内容：' + str(e) + '\n')


if __name__ == '__main__':
    cf = ReadConfig()
    # 设置被叫号码(存储成列表)
    des_phones = cf.get('phonenumber', 'des_phone').split(',')
    # 设置通知日志存储路径
    path_log = cf.get('filepath', 'path_log')
    # 设置异常退信息存储路径
    path_error = cf.get('filepath', 'path_error')