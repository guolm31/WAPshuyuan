#!/usr/bin/python
# coding=utf-8
#edit by guolm 2020-09-08

import os
from configparser import ConfigParser

def ReadConfig(configfile):
    # 获取config.ini文件的位置
    config_file_path = os.path.join(os.path.abspath('..'), 'conf',configfile)
    config = ConfigParser()
    config.read(config_file_path,encoding='utf-8-sig')
    return config