
import sys
sys.path.append('../')
sys.path.append('../lib/')
sys.path.append('../lib/smpplib/')
import os
import time
import lib.smpp as smpp
import logging
import lib.logger as logger

from lib.readconfig import ReadConfig
cf = ReadConfig('config.ini')
smpp_host = cf.get('smpp', 'host')
smpp_port = cf.get('smpp', 'port')
smpp_user = cf.get('smpp', 'user')
smpp_passwd = cf.get('smpp', 'passwd')

# 设置程序间隔时间
sleep_time = cf.getint('checkftp', 'check_sleep')
# 设置读取文件保存路径
path_read = cf.get('checkftp','checkftp_path')

org = cf.get('checkftp','check_org')
des= cf.get('checkftp','check_des').split(',')
ftplist = cf.get('checkftp','check_list').split(',')

if __name__ == '__main__':
    mylogger = logger.Logger()
    logging.debug(smpp_host + "  " + smpp_port + "  " + smpp_user + "  " + smpp_passwd)
    while True:
        try:
            files=os. listdir(path_read)  # 得到文件夹下的所有文件名称,得到的是一个列表
            if not files:
                for i in des:
                    #S.sendoneline(org, '全部设备FTP异常', i, tsleep=0.2)  # 通知  全部设备FTP异常
                    print(org,i,'全设备异常')
            else:
                filename = []
                for file in files:
                    file_ip = file[:-4]
                    filename.append(file_ip)
                for file_n in ftplist:
                    if file_n in filename:
                        os.remove(path_read+ '/'+file_n+'.txt' )
                    else:
                        for i in des:
                            #S.sendoneline(org, '设备{0}FTP异常'.format(file),i, tsleep=0.2)
                            print('设备{0},FTP异常'.format(file_n),org,i)
        except Exception as e:
            logging.error("smpp连接短信中心失败:%s" % e)

        time.sleep(sleep_time)

