#!/usr/local/bin/python
# coding:utf-8
#edit by guolm 2020-09-08

import sys
sys.path.append('../')
sys.path.append('../lib/')
sys.path.append('../lib/smpplib/')
import time
import os
from lib.readconfig import ReadConfig
import lib.smpp as smpp
import lib.logger as logger
import logging

cf = ReadConfig('config_server.ini')
#smpp参数
smpp_host = cf.get('smpp', 'host')
smpp_port = cf.get('smpp', 'port')
smpp_user = cf.get('smpp', 'user')
smpp_passwd = cf.get('smpp', 'passwd')
# 设置程序间隔时间
sleep_time = cf.getint('interval', 'sleeptime')
# 设置读取文件保存路径
path_read = cf.get('filepath','path_read')


def send(org_phone,msg,des_phone):
    #初始化smpp连接
    S = smpp.SmppSendMSG(smpp_host, smpp_port, smpp_user, smpp_passwd)
    S.sendoneline(org_phone,msg,des_phone,tsleep=0.2)  # 延时根据短信中心每秒限制设定

if __name__ == "__main__":
    mylogger=logger.Logger()
    while True:
        files=os.listdir(path_read) # 得到文件夹下的所有文件名称,得到的是一个列表
        if not files:
            # 如果没有收到告警文件,将继续定期扫描
            logging.debug('未收到告警文件,继续定期扫描')
            time.sleep(sleep_time)
        else:
            #如果收到告警文件,将读取文件并清空文件夹
            for file in files:
                if not os.path.isdir(file):
                    logging.error("正在处理文件:"+file)
                    with open(path_read + '/' + file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        users = []
                        for line in lines:
                            for word in line.split(","):
                                users.append(word)
                            #print(users[2])  # 对应send函数的org_phone
                            #print(users[1])  # 对应send函数的msg
                            #print(users[3])  # 对应send函数的des_phone
                            logging.error("发送短信:  主叫:"+users[2]+" 内容:"+users[1]+" 被叫:"+users[3])
                            send(users[2], users[1], users[3])
                    logging.error("文件处理完毕，删除"+file)
                    os.remove(path_read + '/' + file)


