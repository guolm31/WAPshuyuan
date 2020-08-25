import lib.logger as logger
import logging
import lib.smpp as smpp

class Test():
    def __init__(self):
        logg=logger.Logger()
        logging.debug('this is a init debug from test.py')
    def do(self):
        logging.debug('this is a do debug from test.py')




test1=Test()
test1.do()

def main(msg,msisdns):
    cfg = {
        'host' : '10.222.45.24', 'port' : 5016 ,
        'user' : 'YJDX', 'passwd' : 'YJdx!2'
    }
    logging.error(msg)

    S = smpp.SmppSendMSG(cfg['host'], cfg['port'], cfg['user'], cfg['passwd'])
    S.sendgroup(msg,msisdns,tsleep=0.2)  # 延时根据短信中心每秒限制设定

if __name__ == "__main__":
    msg_test = ("你好hello123")
    m_list = []
    m_list.append('18607181232')
    main(msg_test,m_list)
#dddd

