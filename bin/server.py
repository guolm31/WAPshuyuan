#!/usr/local/bin/python
# coding:utf-8

import time
import os
from lib.readconf import ReadConfig
import lib.smpp as smpp
import lib.logger as logger
import logging


def isFindTxt(path):  # 查找指定目录，判断是否有文件，有的话，return table
    cf = ReadConfig()
    #sleep_time = int(cf.get('interval', 'sleeptime'))   # 设置程序间隔时间
    while 1:
        if not os.listdir(path):
            print('未收到告警文件,继续定期扫描')
            #time.sleep(sleep_time)
        else:
            message_table = []
            print('收到告警文件,将读取文件并清空文件夹')
            files = os.listdir(path)  # 得到文件夹下的所有文件名称,得到的是一个列表
            for file in files:
                if not os.path.isdir(file):
                    with open(path + '/' + file, 'r', encoding='gbk') as f:
                        lines = f.readlines()
                        users = []
                        for line in lines:
                            for aa in line.split(","):
                                users.append(aa)
                            print(users[2])   #对应send函数的org_phone
                            print(users[1])   #对应send函数的msg
                            print(users[3])   #对应send函数的des_phone
                            send(users[2],users[1],users[3])
                            line=line.replace("\n","" )
                            message_table.append(line)
                #os.remove(os.fspath(path + '/' + file))  # 删除这个文件
            #if len(message_table) != 0:
            #sendmessage()  # 调用发送短信函数

            return(message_table)
        #time.sleep(sleep_time)

def send(org_phone,msg,des_phone):
    cf = ReadConfig()
    smpp_host = cf.get('smpp', 'host')
    smpp_port = cf.get('smpp', 'port')
    smpp_user = cf.get('smpp', 'user')
    smpp_passwd = cf.get('smpp', 'passwd')
    #org_phone = cf.get('phonenumber', 'org_phone')
    # 设置被叫号码(存储成列表)
    #des_phones = cf.get('phonenumber', 'des_phone').split(',')
    #初始化smpp连接
    S = smpp.SmppSendMSG(smpp_host, smpp_port, smpp_user, smpp_passwd)
    S.sendoneline(org_phone,msg,des_phone,tsleep=0.2)  # 延时根据短信中心每秒限制设定

if __name__ == "__main__":
    #path=int(cf.get('filepath', 'path_mesaage'))
    path = input('请输入文件目录路径')  #r"C:\Users\王少敏\Desktop\python实践\log"
    print(isFindTxt(path))
