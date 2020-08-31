# -*- coding: utf-8 -*-

import os
import time
import logging

class Logger():
    def __init__(self):
        LOGFILE = '../log/debug_' + time.strftime("%Y%m%d")+'.log'
        file_handler = logging.FileHandler(filename=LOGFILE, mode='a', encoding='utf-8', )
        console_handler=logging.StreamHandler()
        logging.basicConfig(
            format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[file_handler,console_handler,],
            level=logging.ERROR)

def main():
    mylogger=Logger()
    logging.debug('this is a debug from Logger.py')

#当.py文件被直接运行时，if __name__ == '__main__'之下的代码块将被运行；
#当.py文件以模块形式被导入时，if __name__ == '__main__'之下的代码块不被运行。
if __name__ == "__main__":
    main()










