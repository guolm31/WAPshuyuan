#!/usr/local/bin/python
# coding:utf-8
# author:
# version:build 2020-08-25


import time
import os
import platform
import tarfile
import zipfile
from ftplib import FTP


path = input('请输入文件目录路径')  #定期扫描日志目录中的文件r"C:\Users\Administrator\Desktop\log"

def isFindTxt(path):  # 查找指定目录，判断是否有文件，有的话，return table
    while 1:
        if not os.listdir(path):
            print('日志目录没有文件,继续定期扫描')
            time.sleep(60 * 60)
        else:
            print('日志目录有文件,将文件ftp到服务器并备份到备份目录')
            os_name = platform.system()
            today = time.strftime('%Y%m%d')
            now = time.strftime('%Y%m%d_%H%M%S')

            app_name = 'sxhbc'

            bak_dir = r'C:\Users\Administrator\Desktop\log'            #日志目录地址
            bak_src = [r'C:\Users\Administrator\Desktop\bak']   #备份目录地址

            keep_days = '90'

            # ftp settings ftp服务器配置
            ftp_server = '*.*.*.*'
            ftp_port = '21'
            ftp_user = 'user'
            ftp_password = 'passwd'
            # -------------------------------------------------------------------------------
            bak_dest = '%s/%s' % (bak_dir, app_name)
            bak_web = '%s/webapps' % (bak_dest)

            prefix = app_name
            log_file = '%s_%s.log' % (prefix, now)
            log_dest = '%s/%s' % (bak_dest, log_file)
            zip_file = '%s_%s.tar.gz' % (prefix, now)
            zip_dest = '%s/%s' % (bak_dest, zip_file)

            ###############################################################################
            def execute_cmd(cmd):
                if 0 != os.system(cmd):
                    print
                    '!!!!!!!!!!ERROR, Please check your command --> %s' % (cmd)

            def backup_files(src, dest):
                if not os.path.exists(dest):
                    os.makedirs(dest)
                cmd_copy = 'xcopy "%s" "%s" /I /Y /S /D >> %s' % (src, dest, log_dest)
                if (os_name == 'Linux'):
                    cmd_copy = 'cp -ruv %s, %s >> %s' % (src, dest, log_dest)
                print(cmd_copy)
                execute_cmd(cmd_copy)

            def tar_files(src, dest):
                print('taring files to %s...' % (dest))
                tar = tarfile.open(dest, 'w:gz')
                tar.add(src, os.path.basename(src))
                tar.close()

            def ftp_stor_files(file):
                cmd_stor = "STOR %s" % (os.path.split(file)[1])
                print(cmd_stor)
                ftp = FTP(ftp_server, ftp_user, ftp_password)
                print(ftp.getwelcome())
                ftp.storbinary(cmd_stor, open(file, "rb"), 1024)
                ftp.close()

            def clear_files():
                # os.remove(dump_dest)

                cmd_clear = 'forfiles /s /p %s /m *.tar.gz /d -%s /c "cmd /c del @file"' % (
                bak_dest.replace('/', '\\'), keep_days)
                if (os_name == 'Linux'):
                    cmd_clear = '/usr/bin/find %s -mtime +%s -name "*.tar.gz" -exec /usr/bin/rm -rf {} %s' % (
                    bak_dest, keep_days, '''\;''')
                print(cmd_clear)
                execute_cmd(cmd_clear)

            if __name__ == '__main__':
                backup_files(' '.join(bak_src), bak_web)
                # tar_files(bak_web, zip_dest)
                # ftp_stor_files(zip_dest)
                clear_files()
                print('done, pyhon is great!')

    time.sleep(60 * 60)

