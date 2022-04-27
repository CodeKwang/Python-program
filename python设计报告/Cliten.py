# coding=utf-8
import re
import time
import socket
import threading
import tkinter as tk
import tkinter.scrolledtext as tst
from DU import *
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog


# 注册界面类
class registerGUI(object):
    def __init__(self, master=None):
        self.root = master
        self.root.title("注册")  # 标题
        self.root.geometry('300x300+700+100')  # 界面大小，出现的位置
        self.createPage()

    # 建立界面函数
    def createPage(self):
        self.page = tk.Frame(self.root)  # 创建Frame框架
        self.page.pack()  # 显示框架
        canvas = tk.Canvas(self.page, width=300, height=300, bd=0, highlightthickness=0)  # 创建画布
        photo = tk.PhotoImage(file=r'.\picture\register.png')  # 注册界面背景图片
        canvas.create_image(150, 150, image=photo)
        canvas.pack()
        self.user = tk.Label(self.page, text="用户名", bg='#F8F8FF')  # 用户名
        self.password1 = tk.Label(self.page, text="密码", bg='#F8F8FF')  # 密码
        self.password2 = tk.Label(self.page, text="确定密码", bg='#F8F8FF')  # 确定密码
        self.e1 = tk.Entry(self.page)  # 用户名输入框，限定为5位的数字
        self.e2 = tk.Entry(self.page, show="*")  # 密码输入框， 密码以*显示，限定为6位的数字
        self.e3 = tk.Entry(self.page, show="*")  # 确定密码输入框，确定密码以*显示
        self.user.place(x=10, y=30, width=45, height=40)  # 用户名位置
        self.password1.place(x=10, y=90, width=45, height=40)  # 密码位置
        self.password2.place(x=0, y=150, width=55, height=40)  # 确定密码位置
        self.e1.place(x=60, y=30, width=200, height=40)  # 用户名输入框位置
        self.e2.place(x=60, y=90, width=200, height=40)  # 密码输入框位置
        self.e3.place(x=60, y=150, width=200, height=40)  # 确定密码输入框位置
        self.button = tk.Button(self.page, text='立即注册', bg='#00BFFF', fg='#FFFFFF',
                                command=self.sure)  # 立即注册按钮，调用函数sure
        self.button.place(x=100, y=200, width=100, height=40)  # 按钮位置
        self.page.mainloop()  # 界面显示

    def sure(self):
        user = self.e1.get()  # 获取用户名
        pa1 = self.e2.get()  # 获取密码
        pa2 = self.e3.get()  # 获取确定密码
        # print(pa1,pa2)
        if user == '' or pa1 == '' or pa2 == '':  # 判断用户名、密码、确定密码是否有空
            messagebox.showwarning(title='警告', message='有输入框为空！')  # 若有空，出现警告框
        elif pa1 is pa2:  # 比较密码和确定密码是否相同
            messagebox.showwarning(title='警告', message='二次密码不相同！')  # 若不相同，出现警告框
        else:
            str = '2' + user + pa2
            sendMessage = bytes(str, encoding='utf8')  # 将数据处理为'utf8'
            client.send(sendMessage)  # 发送输入的数据
            recMsg = client.recv(1024).decode("utf-8")  # 接收数据，编码为'utf-8'
            if 'register' in recMsg:  # 接收数据中包含有注册成功的标志字符串’register‘
                messagebox.showinfo(title='提示', message='注册成功！')  # 若注册成功，出现提示框
                self.page.destroy()  # 框架删除
                sign(self.root)  # 调用登录界面类
            elif 'nor' in recMsg:  # 接收数据中包含有注册不成功的标志字符串’nor‘
                messagebox.showwarning(title='警告', message='用户已存在！')  # 若注册不成功，出现警告框


# 登录界面类
class sign(object):
    def __init__(self, master=None):
        self.root = master
        self.root.geometry("380x234+700+100")  # 界面大小，出现的位置
        self.creatPage()

    # 建立界面函数
    def creatPage(self):
        self.page = tk.Frame(self.root)  # 建立框架
        self.page.pack()
        canvas = tk.Canvas(self.page, width=380, height=234, bd=0, highlightthickness=0)  # 建立画布
        photo = tk.PhotoImage(file=r'.\picture\sign.png')  # 登录界面背景图片
        canvas.create_image(190, 117, image=photo)
        canvas.pack()
        self.user = tk.Label(self.page, text="用户名", bg='#F8F8FF')  # 用户名
        self.password = tk.Label(self.page, text="密码", bg='#F8F8FF')  # 密码
        self.e1 = tk.Entry(self.page)  # 用户名输入框，限定为5位的数字字符串
        self.e2 = tk.Entry(self.page, show="*")  # 密码输入框， 密码以*显示，限定为6位的数字字符串
        self.user.place(x=50, y=30, width=45, height=40)  # 用户名位置
        self.password.place(x=50, y=90, width=45, height=40)  # 密码位置
        self.e1.place(x=100, y=30, width=200, height=40)  # 用户名输入框位置
        self.e2.place(x=100, y=90, width=200, height=40)  # 密码输入框位置
        # self.e1.insert(0, "00001")
        # self.e2.insert(0, "123456")
        self.button1 = tk.Button(self.page, text='登录', bg='#00BFFF', fg='#FFFFFF', command=self.sign)  # 登录按钮
        self.button1.place(x=40, y=180, width=60, height=40)  # 登录按钮位置
        self.button2 = tk.Button(self.page, text='注册', bg='#00BFFF', fg='#FFFFFF', command=self.register)  # 注册按钮
        self.button2.place(x=270, y=180, width=60, height=40)  # # 注册按钮
        self.page.mainloop()  # 框架显示

    # 登录函数
    def sign(self):
        # print(u)
        u = self.e1.get()  # 获取用户名
        p = self.e2.get()  # 获取密码
        if u == '' or p == '':
            messagebox.showwarning(title='警告', message='输入为空！')  # 若登录不成功，出现警告框
        else:
            self.upSend(u, p)  # 调用用户名和密码发送函数

    # 注册函数
    def register(self):
        self.page.destroy()  # 框架删除
        registerGUI(self.root)  # 调用注册界面类

    # 用户名和密码发送函数
    def upSend(self, u, p):
        str = '1' + u + p
        sendMessage = bytes(str, encoding='utf8')  # 将数据处理为'utf8'
        client.send(sendMessage)  # 发送输入的数据
        recMsg = client.recv(1024).decode("utf-8")  # 接收数据，编码为'utf-8'
        if 'sign' in recMsg:  # 接收数据中包含有登录成功的标志字符串’sign‘
            messagebox.showinfo(title='提示', message='登录成功！')  # 若登录成功，出现提示框
            self.page.destroy()
            chatUI(self.root)
        elif 'nos' in recMsg:  # 接收数据中包含有登录不成功的标志字符串’nos‘
            messagebox.showwarning(title='警告', message='用户登录错误！')  # 若登录不成功，出现警告框


# 聊天界面类
class chatUI(object):
    def __init__(self, master):
        self.root = master
        self.root.geometry("700x800+800+0")  # 界面大小，出现的位置
        self.creatPage()

    # 建立界面函数
    def creatPage(self):
        self.page = tk.Frame(self.root)  # 创建Frame框架
        self.page.pack()
        canvas = tk.Canvas(self.page, width=700, height=800, bd=0, highlightthickness=0)  # 创建画布
        canvas.pack()
        self.textEdit = tst.ScrolledText(self.page)  # 聊天信息显示框
        self.textEdit.place(x=0, y=0, width=550, height=650)  # 聊天信息显示框位置
        self.textEdit.tag_config('time', foreground='blue')  # 定义标签，改变字体颜色
        self.inputText = tk.Text(self.page, width=80, height=5)  # 信息编辑框
        self.inputText.place(x=0, y=650, width=550, height=150)  # 信息编辑框位置
        self.inputText.bind("<KeyPress-Return>", self.textSendReturn)  # 定义快捷键，按下回车即可发送消息
        self.btnSend = tk.Button(self.page, text='发送', bg='#00BFFF', fg='#FFFFFF', command=self.textSend)  # 发送按钮
        self.btnSend.place(x=470, y=740, width=60, height=40)  # 发送按钮位置
        self.l1 = tk.Label(self.page, text='群文件')  # 群文件
        self.l1.place(x=550, y=0, width=60, height=40)  # 群文件位置
        self.button1 = tk.Button(self.page, text='上传', bg='#00BFFF', fg='#FFFFFF', command=self.upfile)  # 上传按钮
        self.button1.place(x=635, y=0, width=60, height=40)  # 上传按钮位置
        self.L1 = tk.Listbox(self.page)  # 群文件列表
        self.L1.place(x=550, y=40, width=145, height=360)  # 群文件列表位置
        self.button1 = tk.Button(self.page, text='下载', bg='#00BFFF', fg='#FFFFFF', command=self.downfile)  # 下载按钮
        self.button1.place(x=635, y=360, width=60, height=40)  # 下载按钮位置
        self.l2 = tk.Label(self.page, text='群成员')  # 群成员
        self.l2.place(x=550, y=400, width=60, height=40)  # 群成员位置
        self.L2 = tk.Listbox(self.page)  # 群成员列表
        self.L2.place(x=550, y=440, width=145, height=360)  # 群成员列表位置
        # 开启一个线程用于接收消息并显示在聊天窗口
        t = threading.Thread(target=self.getInfo)
        t.start()
        self.inputText.insert(tk.END, 'lookf')  # 显示聊天界面时，发送查看群文件标志字符串lookf，获取群文件列表
        self.textSend()

    # 发送输入框的内容
    def textSend(self):
        # 获取Text的所有内容
        str = self.inputText.get('1.0', tk.END)
        if str.strip() != '':
            self.textEdit.see(tk.END)  # 将滚动条拉到最后显示最新消息
            self.inputText.delete(0.0, tk.END)  # 删除输入框的内容
            sendMessage = bytes(str, encoding='utf8')  # 将数据处理为”utf8“
            client.send(sendMessage)  # 发送数据到服务端
        else:
            tk.messagebox.showinfo('警告', "不能发送空白信息！")  # 若编辑框为空，出现警告框

    # 接受服务器的信息
    def getInfo(self):
        global client
        while True:
            # 接收数据,1024指定缓存长度，使用的是recv方法
            recMessage = client.recv(1024).decode("utf8") + '\n'  # 获取数据
            if 'upf' in recMessage:  # 若接收字符串包含上传成功的标志字符串'upf',弹出提示框
                messagebox.showinfo(title='提示', message='上传成功！')
            elif 'downf' in recMessage:  # 若接收字符串包含下载成功的标志字符串'downf',弹出提示框
                messagebox.showinfo(title='提示', message='下载成功！')
            elif 'fl' in recMessage:  # 若接收字符串包含群文件标志字符串'fl',更新群文件列表
                rec = recMessage.splitlines()  # 字符串按行分割
                self.L1.delete(0, tk.END)  # 删除群文件列表
                for i in range(len(rec) - 2):  # 重新群文件列表
                    self.L1.insert(i, rec[i + 1])
            elif 'use' in recMessage:  # 若接收字符串包含用户列表标志字符串'use',更新用户列表
                rec = recMessage.splitlines()  # 字符串按行分割
                self.L2.delete(0, tk.END)  # 删除用户列表
                for i in range(len(rec) - 2):  # 重新写用户列表
                    self.L2.insert(i, rec[i + 1])
            else:  # 其他信息，就显示在聊天信息显示框
                recTime = time.strftime('%Y-%m-%d %H:%M', time.localtime()) + '\n'  # 获取当前时间
                self.textEdit.insert(tk.END, recTime, 'time')  # time作为标签,改变字体颜色
                self.textEdit.insert(tk.END, recMessage)  # 将聊天信息加入聊天信息显示框位置
                self.textEdit.see(tk.END)  # 将滚动条拉到最后显示最新消息

    # 上传文件
    def upfile(self):
        try:
            filepath = filedialog.askopenfilename()  # 打开文件选择框
            r = r'[^.\\/:*?"<>|\r\n]+\.[^.\\/:*?"<>|\r\n]+$'
            s = re.findall(r, filepath)  # 正则表达式匹配文件名
            try:
                if UpLoadFile(filepath, s[0]) == True:  # 调用上传函数
                    self.inputText.insert(tk.END, 'upf')  # 发送上传成标志字符串upf给服务器
                    self.textSend()
                else:
                    messagebox.showinfo(title='警告', message='文件上传不成功！')  # 上传不成功
            except ConnectionRefusedError:
                messagebox.showinfo(title='警告', message='服务器未打开！')  # 出现错误，出现警告框
        except:
            messagebox.showwarning(title='警告', message='未选择文件！')  # 未选择文件，出现警告框

    # 下载文件
    def downfile(self):
        try:
            global inde
            for i in self.L1.curselection():  # 遍历L1列表
                inde = self.L1.get(i)
            folderpath = filedialog.askdirectory()  # 打开下载到的文件夹
            try:
                if DownLoadFile(folderpath + '/' + inde, './' + inde) == True:  # 调用文件下载函数
                    self.inputText.insert(tk.END, 'downf')  # 发送下载成功标志字符串downf给服务器
                    self.textSend()
                else:
                    messagebox.showinfo(title='警告', message='文件下载不成功！')  # 下载不成功
            except ConnectionRefusedError:
                messagebox.showinfo(title='警告', message='服务器未打开！')  # 出现错误，出现警告框
        except:
            messagebox.showwarning(title='警告', message='未选择文件！')  # 未选择文件，出现警告框

    # 按下回车即可发送消息
    def textSendReturn(self, event):
        if event.keysym == "Return":
            self.textSend()


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 建立套接字
    IP = "127.0.0.1"  # IP地址
    PORT = 7890  # 端口号
    client.connect((IP, PORT))  # 建立连接
    root = tk.Tk()  # 创建界面
    root.title("KK聊天室")  # 标题
    im = Image.open(r'.\picture\tubiao.ico')  # 导入图标
    img = ImageTk.PhotoImage(im)
    root.tk.call('wm', 'iconphoto', root._w, img)  # 将图标法放入界面
    sign(root)  # 调用sign登录界面类
    root.mainloop()  # 界面显示
