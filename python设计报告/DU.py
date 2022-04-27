# coding=utf-8
import os
from ftplib import FTP

'''
文件下载函数
LocalFile：文件下载到位置
RemoteFile：从服务端下载的位置
'''


def DownLoadFile(LocalFile, RemoteFile):
    try:
        ftp = FTP('10.2.171.72')  # 连接服务器的IP地址
        ftp.encoding = 'utf-8'  # 编码方式utf-8
        ftp.login('user', '123')  # 登录服务器
        file_handler = open(LocalFile, 'wb')  # 打开文件夹
        ftp.retrbinary("RETR %s" % (RemoteFile), file_handler.write)  # 下载文件
        file_handler.close()  # 关闭文件夹
        return True  # 返回True
    except:
        return False  # 返回False


'''
文件上传函数
LocalFile：上传文件的位置
RemoteFile：上传到服务端的位置
'''


def UpLoadFile(LocalFile, RemoteFile):
    try:
        ftp = FTP('10.2.171.72')  # 连接服务器的IP地址
        ftp.encoding = 'utf-8'  # 编码方式utf-8
        ftp.login('user', '123')  # 登录服务器
        if not os.path.isfile(LocalFile):  # 用于判断某一对象(需提供绝对路径)是否为文件
            return False
        file_handler = open(LocalFile, "rb")  # 打开文件
        ftp.storbinary('STOR %s' % RemoteFile, file_handler, 4096)  # 上传文件
        file_handler.close()  # 关闭文件
        return True  # 返回True
    except:
        return False  # 返回False
