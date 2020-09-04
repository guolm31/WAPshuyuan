#!/usr/bin/python
# coding=utf-8

import logging

import lib.logger as logger
import lib.smpp as smpp
from lib.readconf import ReadConfig



def send(msg):
    logg = logger.Logger()
    cf = ReadConfig()
    smpp_host = cf.get('smpp', 'host')
    smpp_port = cf.get('smpp', 'port')
    smpp_user = cf.get('smpp', 'user')
    smpp_passwd = cf.get('smpp', 'passwd')
    org_phone = cf.get('phonenumber', 'org_phone')
    # 设置被叫号码(存储成列表)
    des_phones = cf.get('phonenumber', 'des_phone').split(',')
    S = smpp.SmppSendMSG(smpp_host, smpp_port, smpp_user, smpp_passwd)
    S.sendsms(org_phone,msg,des_phones,tsleep=0.2)  # 延时根据短信中心每秒限制设定

if __name__ == "__main__":
    send("你好")
    logging.error("发送成功")
#dddd

