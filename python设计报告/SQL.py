# coding=utf-8
import sqlite3


# 登录验证函数
def is_user(username, password):
    conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\python设计报告\userdb.db')  # 连接数据库
    cur = conn.execute('')  # 建立游标
    # 根据用户名和密码在数据库中表进行查询
    cur.execute("select username,password from users where username={} and password={}".format(username, password))
    if len(cur.fetchall()):  # 若查询到用户名和对应密码，则返回True
        conn.commit()
        cur.close()  # 关闭游标
        conn.close()  # 关闭连接
        return True
    else:  # 若未查询到用户名和相应密码，则返回False
        conn.commit()
        cur.close()  # 关闭游标
        conn.close()  # 关闭连接
        return False


# 用户名和密码写入数据库
def add_user(username, password):
    conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\python设计报告\userdb.db')  # 连接数据库
    # 若存在表，则直接加入，不存在表，就创建表后，再加入
    cur = conn.execute("create table if not exists users(username string primary key,password string)")  # 创建游标
    try:
        cur.execute("insert into users(username,password)values(?,?)", (username, password))  # 加入用户名和密码
        conn.commit()
        cur.close()  # 关闭游标
        conn.close()  # 关闭连接
        return True  # 返回True
    except sqlite3.IntegrityError:  # 若用户名已存在，则返回False
        return False


if __name__ == '__main__':
    add_user('00001', '123456')
    # print(is_user('00002','123456'))
