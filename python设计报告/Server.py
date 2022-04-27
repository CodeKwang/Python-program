# coding=utf-8
import os
import SQL
import queue
import socket
import os.path
import threading

IP = '127.0.0.1'  # ip地址
PORT = 7890  # 端口
messages = queue.Queue()  # 存放群发的信息的队列 一对多
users = []  # 群成员列表 0:用户名 1:connection
scMess = []  # 存放客户端与服务器交互信息的列表 一对一
lock = threading.Lock()  # 线程互斥锁


# 统计当前在线人员
def onlines():
    online = []
    for i in range(len(users)):
        online.append(users[i][0])
    return online


# 服务器类，继承threading.Thread类
class chatServer(threading.Thread):
    global users, lock, messages  # 全局变量

    # 构造函数
    def __init__(self):
        threading.Thread.__init__(self)  # 调threading.Thread类构造函数
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 建立tcp套接字

    # 接收客户端消息
    def receive(self, conn, addr):
        recMsg = conn.recv(1024).decode("utf-8")  # 接受客户端登录或注册信息
        user = ''
        try:
            num = ''  # 用户名和用户密码都为数字，用户名长度为5，密码长度为6
            for i in recMsg:
                if i.isdigit():
                    num = num + i
            user = num[1:6]  # 用户名，长度为5
            pw = num[6:12]  # 用户密码，长度为6
            # 判断第一位数字，若为1，则进行查询数据库中是否有该用户；若为2，则进行将用户名字和密码写入数据库中
            if num[0] == '1':
                if SQL.is_user(user, pw):  # 查询数据库中是否有该用户
                    users.append((user, conn))  # 将用户名user和连接conn 加入用户列表users
                    st = 'sign'
                    scMess.append((st, conn))  # 将登录成功sign标志字符加入客户端与服务器交互信息的列表
                else:
                    st = 'nos'
                    scMess.append((st, conn))  # 将登录不成功nos标志字符加入客户端与服务器交互信息的列表
            elif num[0] == '2':
                if SQL.add_user(user, pw):  # 将用户名字和密码写入数据库中
                    st = 'register'
                    scMess.append((st, conn))  # 将注册成功register标志字符加入客户端与服务器交互信息的列表
                else:
                    st = 'nor'
                    scMess.append((st, conn))
        except:
            pass
        USERS = onlines()  # 调用获取所有用户的函数
        str = 'use\n'  # 表示所有用户标志字符串use
        for i in USERS:  # 将用户名加入字符串str
            str = str + i + '\n'
        self.Load(str, addr)  # 将包含所有用户名的字符串加入存放群发的信息的队列
        # 在获取用户名后便会不断地接收用户端发来的消息（即聊天内容），结束后关闭连接。
        try:
            while True:
                message = conn.recv(1024).decode("utf-8")  # 接收消息
                if 'lookf' in message:  # 若客户端发送信息中包含查看群文件标志字符串lookf，则将获取全部群文件名，并加入存放群发的信息的队列
                    lis = self.filelist()  # 调用获取全部群文件名称的函数
                    str = 'fl\n'  # 表示群文件的标志字符串fl
                    for i in lis:  # 将群文件名加入字符串str
                        str = str + i + '\n'
                    self.Load(str, addr)  # 将包含全部群文件名的字符串加入存放群发的信息的队列
                elif 'upf' in message:  # 若客户端发送信息中包含上传文件的标志字符串upf，则将字符串upf发送给客户端，表示上传成功，并同时重新获取全部群文件名并发送
                    str = 'upf'  # 表示文件上传成功标志字符串upf
                    scMess.append((str, conn))  # 将字符串加入客户端与服务器交互信息的列表
                    lis = self.filelist()  # 调用获取全部群文件名称的函数
                    str = 'fl\n'  # 表示群文件的标志字符串fl
                    for i in lis:  # 将群文件名加入字符串str
                        str = str + i + '\n'
                    self.Load(str, addr)  # 将包含全部群文件名的字符串加入存放群发的信息的队列
                elif 'downf' in message:  # 若客户端发送信息中包含下载文件的标志字符串downf，则将字符串downf发送给客户端，表示下载成功
                    str = 'downf'  # 表示文件下载成功标志字符串downf
                    scMess.append((str, conn))  # 将字符串加入客户端与服务器交互信息的列表
                else:  # 其他没包含上面的标志字符串的信息正常处理
                    message = user + ':' + message  # 在信息前加上信息发出用户的用户名
                    self.Load(message, addr)  # 将字符串加入存放群发的信息的队列
            # conn.close() # 关闭连接
        # 如果用户断开连接，将该用户从用户列表中删除，然后更新用户列表。
        except:
            j = 0
            for man in users:
                if man[0] == user:
                    users.pop(j)  # 服务器删除退出的用户
                    break
                j = j + 1
            USERS = onlines()
            self.Load(USERS, addr)
            conn.close()

    # 获取群文件夹中文件名
    def filelist(self):
        filelis = os.listdir(r'.\filedir')
        return filelis

    # 将地址与信息（需发送给客户端）存入messages队列
    def Load(self, data, addr):
        lock.acquire()  # 获取锁
        try:
            messages.put((addr, data))  # 将地址与信息加入messages队列
        finally:
            lock.release()  # 释放锁

    # 服务端在接受到数据后，会对其进行一些处理然后发送给客户端，对于聊天内容，服务端群发给客户端，对于登录，注册，上传，下载的信息要服务器一对一发送
    def sendData(self):
        global scMess
        while True:
            if not messages.empty():  # 队列messages不空时
                message = messages.get()  # 获取messages内容
                for i in range(len(users)):  # 向所有用户发送信息
                    data = ' ' + message[1]
                    users[i][1].send(data.encode('utf-8'))
            if scMess:  # 向对应用户发送信息
                for i in range(len(scMess)):
                    scMess[i][1].send(scMess[i][0].encode('utf-8'))
                scMess = []  # 将列表置空

    # 重写threading.Thread类的run函数，实现多线程
    def run(self):
        self.s.bind((IP, PORT))  # 监听本机7890端口
        self.s.listen(5)  # 连接最大数为5
        q = threading.Thread(target=self.sendData)  # 线程用于发送
        q.start()
        while True:
            conn, addr = self.s.accept()  # 接受一个新连接
            t = threading.Thread(target=self.receive, args=(conn, addr))  # 线程用于接收
            t.start()
        # self.s.close() # 关闭套接字


if __name__ == '__main__':
    cserver = chatServer()  # 调用服务器类
    cserver.start()
