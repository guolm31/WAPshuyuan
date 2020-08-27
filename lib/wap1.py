#!/usr/bin/python
# coding=utf-8
import os
import datetime
import time
from readconf import ReadConfig


def file_monitor():
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

    # 循环判断程序
    while True:
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
            if int(num) > 5:
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

            # 设置休眠时间
            time.sleep(sleep_time)

        except Exception as e:
            time_break = datetime.datetime.now()
            file_break = time_break.strftime('%Y%m%d%H%M%S')

            # 生成监控程序退出告警
            with open(r'{0}/{1}.txt'.format(path_log, file_break), 'w')as f:
                for des_phone in des_phones:
                    text_break = '{0},监控程序异常退出,{1},{2}\n'.format(time_break.strftime('%Y-%m-%d %H:%M:%S'), org_phone,
                                                               des_phone)
                    f.write(text_break)
            # 存储异常信息
            with open(r'{0}/{1}.txt'.format(path_error, 'error' + file_break), 'w')as f:
                f.write(str(e))
            print(e)


if __name__ == '__main__':
    file_monitor()
