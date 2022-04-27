# Python-program
Python小项目
## Python设计报告
基于多线程与FTP文件共享服务器的聊天室开发程序设计
### 功能如下：
1、登陆界面注册界面和聊天室界面的布局设置
2、注册功能的实现
3、登录功能
4、上传下载文件功能
5、多线程功能实现
### server.py 服务器
```python
# 服务器类，继承threading.Thread类
class chatServer(threading.Thread):
```

### client.py 客户端
```python
# 注册界面类
class registerGUI(object):

# 登录界面类
class sign(object):

# 聊天界面类
class chatUI(object):
```
### userdb.db 用户数据库
存储注册用户名和密码

### SQL.py 登录验证和注册
```python
# 登录验证函数
def is_user(username, password):

# 用户名和密码写入数据库
def add_user(username, password):
```

### FTPserver.py FTP文件服务器
搭建FTP文件共享服务器

### DU.py 文件上传下载
```python
# 文件下载函数
def DownLoadFile(LocalFile, RemoteFile):

# 文件上传函数
def UpLoadFile(LocalFile, RemoteFile):
```
