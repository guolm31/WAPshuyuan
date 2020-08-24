#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
#import paramiko
import time
import datetime
from optparse import OptionParser


import sys
import smpplib.gsm
import smpplib.client
import smpplib.consts
import threading
import logging



# 因短信中心有每秒条数限制，不要用并发，单进程要限制速度。。。。
# 消息发送和接收是异步的，对应关系难搞。。。
import socket
from smpplib import consts, exceptions, smpp

class Client(smpplib.client.Client):

    def read_once(self, ignore_error_codes=None, auto_send_enquire_link=True):
        """Read a PDU and act"""
        try:
            try:
                pdu = self.read_pdu()
            except socket.timeout:
                if not auto_send_enquire_link:
                    raise
                self.logger.debug('Socket timeout, listening again')
                pdu = smpp.make_pdu('enquire_link', client=self)
                self.send_pdu(pdu)
                return

            if pdu.is_error():
                #  这里重写了，不然报错！
                # if pdu.status == 1078:
                #     return
                self.logger.info('pdu error,command: %s, sequence:%s, status: %s'
                                 %(pdu.command,pdu.sequence,pdu.status))
                # return

            if pdu.command == 'unbind':  # unbind_res
                self.logger.info('Unbind command received')
                return
            elif pdu.command == 'submit_sm_resp':
                self.message_sent_handler(pdu=pdu)
            elif pdu.command == 'deliver_sm':
                self._message_received(pdu)
            elif pdu.command == 'query_sm_resp':
                self.query_resp_handler(pdu)
            elif pdu.command == 'enquire_link':
                self._enquire_link_received(pdu)
            elif pdu.command == 'enquire_link_resp':
                pass
            elif pdu.command == 'alert_notification':
                self._alert_notification(pdu)
            else:
                self.logger.warning('Unhandled SMPP command "%s"', pdu.command)
        except exceptions.PDUError as e:
            if ignore_error_codes and len(e.args) > 1 and e.args[1] in ignore_error_codes:
                self.logger.warning('(%d) %s. Ignored.', e.args[1], e.args[0])
            else:
                raise

class SmppSendMSG:
    def __init__(self,host,port,user,passwd):
        try:
            self.client = Client(host, int(port))
            self.client.connect()
            logging.error("IP 端口已连接，开始发送账号密码...")
            self.client.bind_transceiver(system_id=user, password=passwd)
            logging.error("连接短信中心成功！")
        except Exception as e:
            logging.error("连接短信中心失败:%s,退出！"%e)
            sys.exit(1)

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

        parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(msg,
                 encoding=smpplib.consts.SMPP_ENCODING_ISO10646)

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
                if n % 5000 == 0:
                    logging.error("已发送%s条"%n)

        logging.error("短信发送完成,用户数%s,发送拆分短信共条数：%s"%(len(msisdnlist),n))
        logging.error("用时：%s秒，每秒%s条" % (round(time.time() - tt,2), n//(time.time() - tt)))

        a = 0
        # 短信中心发来的消息用用一个子线程监听，死循环，要等一会再回收掉。
        while 1:
            if not thread.isAlive() :
                break
            if a >= 30:
                # 30 秒后直接退出，没收到响应的不等了。。。
                break
            else:
                time.sleep(2)
                a += 2

        try:
            # 这里退出后，子线程会抛异常
            self.client.unbind()
        except Exception as ee:
            logging.error("退出smpp连接报错:%s"%ee)
        # LOGGER.info( "退出smpp连接!")
        sys.exit()

def main(msg,msisdns):
    cfg = {
        'host' : '10.222.45.24', 'port' : 5016 ,
        'user' : 'YJDX', 'passwd' : 'YJdx!2'
    }
    logging.error(msg)
    if not (isinstance(msisdns,list) or isinstance(msisdns,set) or isinstance(msisdns,tuple)):
        logging.error('电话号码表不是list set tuple')
        sys.exit(1)
    logging.error("电话号码数%s"%len(msisdns))

    S = SmppSendMSG(cfg['host'], cfg['port'], cfg['user'], cfg['passwd'])
    S.sendgroup(msg,msisdns,tsleep=0.2)  # 延时根据短信中心每秒限制设定

if __name__ == "__main__":
    msg_test = ("你好hello123")
    m_list = []
    m_list.append('18607181232')
    main(msg_test,m_list)
