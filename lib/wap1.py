#!/usr/bin/python
# coding=utf-8
import os
import datetime
import time


def file_monitor():
    # 设置主叫号码
    org_phone = '6009'
    # 设置被叫号码
    des_phone = '186XXXXXXXX'
    # 设置读取文件数目路径
    # path_read = r'/root/ceshi'
    path_read = r'D:/测试'
    # 设置通知日志存储路径
    path_log = 'D:/测试1'
    # 设置异常退信息存储路径
    path_error = 'D:/测试2'

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
                # 设置文本内容
                text = "{0},{1},{2},{3}".format(time_now.strftime('%Y-%m-%d %H:%M:%S'), error_text, org_phone,
                                                des_phone)

                with open(r'{0}/{1}.txt'.format(path_log, file_error), 'w')as f:
                    f.write(text)

            # 设置休眠时间
            time.sleep(60)

        except Exception as e:
            time_break = datetime.datetime.now()
            file_break = time_break.strftime('%Y%m%d%H%M%S')
            text_break = '{0},监控程序异常退出,{1},{2}'.format(time_break.strftime('%Y-%m-%d %H:%M:%S'), org_phone,
                                                       des_phone)
            # 生成监控程序退出告警
            with open(r'{0}/{1}.txt'.format(path_log, file_break), 'w')as f:
                f.write(text_break)
            # 存储异常信息
            with open(r'{0}/{1}.txt'.format(path_error, 'error' + file_break), 'w')as f:
                f.write(str(e))
            break

if __name__ == '__main__':
    file_monitor()
    #eeeee
