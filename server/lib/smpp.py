#!/usr/bin/env python
# -*- coding:utf-8 -*-


import time
import sys
import threading
import logging
from smpplib import consts, gsm,client

sys.path.append('../')
sys.path.append('../lib/')
sys.path.append('../lib/smpplib/')

from lib.readconfig import ReadConfig
import logger as logger


cf = ReadConfig('../conf/config.ini')
#smpp参数
smpp_host = cf.get('smpp', 'host')
smpp_port = cf.get('smpp', 'port')
smpp_user = cf.get('smpp', 'user')
smpp_passwd = cf.get('smpp', 'passwd')




class SmppSendMSG:
    def __init__(self,host,port,user,passwd):
        try:
            self.client = client.Client(host, int(port))
            self.client.connect()
            logging.error("IP 端口已连接，开始发送账号密码......")
            self.client.bind_transceiver(system_id=user, password=passwd)
            logging.error("连接短信中心成功！")
        except Exception as e:
            logging.error("连接短信中心失败:%s,退出！"%e)

        self.deliverlist = []
        self.sentlist = []
        self.startlist = []

        self.client.set_message_sent_handler( self.message_sent)
        self.client.set_message_received_handler(self.message_received  )

    def message_sent(self,pdu):
        # 发送到短信中心，接收返回消息，不是1070这种状态码，一般就是发送到短信中心完成了
        self.sentlist.append([pdu.sequence, pdu.message_id,pdu.status])

    def message_received(self,pdu):
        # 短信中心下发给用户，成功了就返回0，没成功就一直等待等待...
        # 这个列表没找到数据，就当着发送失败（延迟）
        self.deliverlist.append([pdu.sequence, pdu.status])

    def sendgroup(self,smscontent,msisdnlist,tsleep=0):
        tt = time.time()
        msisdnlist = set(msisdnlist)
        if isinstance(smscontent,str):
            msg = smscontent
        else:
            logging.error("请确保短信消息是UTF8或者UNICODE编码格式")
            return

        thread = threading.Thread(target=self.client.listen, args=())
        thread.setDaemon(True)
        thread.start()

        parts, encoding_flag, msg_type_flag = gsm.make_parts(msg,
                 encoding=consts.SMPP_ENCODING_ISO10646)

        n = 0
        for msisdn in msisdnlist:
            for part in parts:
                pdu = self.client.send_message(
                    source_addr_ton=2,
                    source_addr_npi=1,
                    # Make sure it is a byte string, not unicode:
                    source_addr="6005",

                    dest_addr_ton=1,
                    dest_addr_npi=1,
                    # Make sure thease two params are byte strings, not unicode:
                    destination_addr=str(msisdn).strip(),
                    short_message=part,

                    data_coding=encoding_flag,
                    esm_class=msg_type_flag,
                    registered_delivery=True,
                )
                self.startlist.append([pdu.sequence,pdu.destination_addr])
                n += 1
                time.sleep(tsleep)

        #logging.error("短信发送完成,用户数%s,发送拆分短信共条数：%s"%(len(msisdnlist),n))
        #logging.error("用时：%s秒，每秒%s条" % (round(time.time() - tt,2), n//(time.time() - tt)))

    def sendoneline(self,org_phone,smscontent,msisdn,tsleep=0):
        if isinstance(smscontent,str):
            msg = smscontent
        else:
            logging.error("请确保短信消息是UTF8或者UNICODE编码格式")
            return

        #thread = threading.Thread(target=self.client.listen, args=())
        #thread.setDaemon(True)
        #thread.start()

        parts, encoding_flag, msg_type_flag = gsm.make_parts(msg,
                 encoding=consts.SMPP_ENCODING_ISO10646)

        for part in parts:
            #发送短信send_message
            pdu = self.client.send_message(
                source_addr_ton=2,
                source_addr_npi=1,
                # Make sure it is a byte string, not unicode:
                source_addr=org_phone,
                dest_addr_ton=1,
                dest_addr_npi=1,
                # Make sure thease two params are byte strings, not unicode:
                destination_addr=str(msisdn).strip(),
                short_message=part,
                data_coding=encoding_flag,
                esm_class=msg_type_flag,
                registered_delivery=True,
                )
            #self.startlist.append([pdu.sequence,pdu.destination_addr])
            time.sleep(tsleep)

        #logging.error("短信发送完成,用户数%s,发送拆分短信共条数：%s"%(len(msisdnlist),n))
        #logging.error("用时：%s秒，每秒%s条" % (round(time.time() - tt,2), n//(time.time() - tt)))

    def sendsms(self,org_phone,smscontent,msisdnlist,tsleep=0):
        msisdnlist = set(msisdnlist)
        if isinstance(smscontent,str):
            msg = smscontent
        else:
            logging.error("请确保短信消息是UTF8或者UNICODE编码格式")
            return

        #thread = threading.Thread(target=self.client.listen, args=())
        #thread.setDaemon(True)
        #thread.start()

        parts, encoding_flag, msg_type_flag = gsm.make_parts(msg,
                 encoding=consts.SMPP_ENCODING_ISO10646)

        for msisdn in msisdnlist:
            for part in parts:
                pdu = self.client.send_message(
                    source_addr_ton=2,
                    source_addr_npi=1,
                    # Make sure it is a byte string, not unicode:
                    source_addr=org_phone,
                    dest_addr_ton=1,
                    dest_addr_npi=1,
                    # Make sure thease two params are byte strings, not unicode:
                    destination_addr=str(msisdn).strip(),
                    short_message=part,
                    data_coding=encoding_flag,
                    esm_class=msg_type_flag,
                    registered_delivery=True,
                )
                self.startlist.append([pdu.sequence,pdu.destination_addr])
                time.sleep(tsleep)

        #logging.error("短信发送完成,用户数%s,发送拆分短信共条数：%s"%(len(msisdnlist),n))
        #logging.error("用时：%s秒，每秒%s条" % (round(time.time() - tt,2), n//(time.time() - tt)))

    def disconnect(self):
        self.client.unbind()
        self.client.disconnect()



if __name__ == "__main__":
    mylogger=logger.Logger()
    logging.debug(smpp_host + "  " + smpp_port + "  " + smpp_user + "  " + smpp_passwd)
    # 初始化smpp连接
    while True:
        try:
            S = SmppSendMSG(smpp_host, smpp_port, smpp_user, smpp_passwd)
            S.sendoneline('6009', 'test', '18607181232', tsleep=0.2)
            # 等待5秒，短信SOCKET释放
            S.disconnect()
            time.sleep(5)
        except Exception as e:
            logging.error("连接短信中心失败-smpp-main:%s,退出！" % e)