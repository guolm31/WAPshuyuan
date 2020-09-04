#!/usr/bin/python
# coding=utf-8
import os
from configparser import ConfigParser

def ReadConfig():
    # 获取config.ini文件的位置
    config_file_path = os.path.join(os.path.abspath('..'), 'conf','config.ini')
    config = ConfigParser()
    config.read(config_file_path,encoding='utf-8-sig')
    return config