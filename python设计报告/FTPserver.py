# coding=utf-8
'''
搭建FTP文件共享服务器
'''


from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# 实例虚拟用户
authorizer = DummyAuthorizer()
# 添加用户权限和路径，参数为（用户名，密码，用户目录，权限）
authorizer.add_user('user', '123', r'.\filedir', perm='elradfmwM')
# 初始化句柄
handler = FTPHandler
handler.authorizer = authorizer
# 监听ip和端口
server = FTPServer(('10.2.171.72', 21), handler)
# 开始服务
server.serve_forever()
