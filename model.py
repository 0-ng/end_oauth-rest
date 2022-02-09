import sqlite3
from encryp import computePW, checkPW, createSalt
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "fruit_db.sqlite3")


def get_conn():
    return sqlite3.connect(db_path)


def db_init():
    conn = get_conn()
    print("数据库连接成功")
    cursor = conn.cursor()
    try:
        cursor.execute('''
        CREATE TABLE USER(
            ID INT PRIMARY KEY  NOT NULL,
            USERNAME TEXT NOT NULL,
            PASSWORD TEXT NOT NULL,
            SALT TEXT NOT NULL,
            AUTHORIZATION TEXT NOT NULL,
            TOKEN TEXT NOT NULL);
        ''')
        conn.commit()
    except:
        pass
    cursor.close()
    conn.close()
    admin = User("admin", "admin")
    admin.save()
    user = User("0ng", "123qwe")
    user.save()
    print("用户表创建成功")


class User(object):
    def __init__(self, username, password):
        self.username = username
        salt = createSalt()
        self.password = computePW(password, salt)
        self.salt = salt
        self.authorization = ""
        self.token = ""

    def save(self):
        if User.queryByName(self.username) is None:
            conn = get_conn()
            cursor = conn.cursor()
            sql = "INSERT INTO USER VALUES (?,?,?,?,?,?)"
            cursor.execute(sql, (User.rowCount() + 1, self.username, self.password, self.salt, "", ""))  # 执行sql语句
            conn.commit()  # 提交数据库改动
            cursor.close()  # 关闭游标
            conn.close()  # 关闭数据库连接

    @staticmethod
    def generateAUTHORIZATION(username, rest, web):
        test()
        conn = get_conn()
        cursor = conn.cursor()
        sql = "UPDATE USER SET AUTHORIZATION=?, TOKEN=? where USERNAME=?"
        authorization = createSalt()
        token = f"portal.{rest}.{web}.{username}"
        cursor.execute(sql, (authorization, token, username))
        conn.commit()
        cursor.close()
        conn.close()
        print(username, "generate AUTHORIZATION succeed", authorization)
        return authorization

    @staticmethod
    def getPortalTokenByCode(code):
        conn = get_conn()
        cursor = conn.cursor()
        sql = "SELECT username, token FROM USER WHERE AUTHORIZATION=?"
        username = None
        token = None
        print("get Portal Token By Code", code)
        try:
            print(cursor.execute(sql, (code,)).fetchall().__str__())
            user = cursor.execute(sql, (code,)).fetchall()[0]
            username = user[0]
            token = user[1]
            print(user.__str__())
        except:
            pass
        cursor.close()
        conn.close()
        return username, token

    @staticmethod
    def all():
        sql = "SELECT * FROM USER"
        conn = get_conn()
        cursor = conn.cursor()
        users = cursor.execute(sql).fetchall()
        cursor.close()
        conn.close()
        return users

    @staticmethod
    def queryByName(username):
        sql = "SELECT * FROM USER WHERE username=?"
        conn = get_conn()
        cursor = conn.cursor()
        users = cursor.execute(sql, (username,)).fetchall()
        cursor.close()
        conn.close()
        if len(users) == 0:
            return None
        return users[0]

    @staticmethod
    def rowCount():
        return len(User.all())

    def __str__(self):
        return f'id:{self.id}--name:{self.username}'  # 注此处的是点不是逗号


def test():
    respEnv = {
        "portal_rest": 'B',
        "portal_web": 'B'
    }
    f(respEnv["portal_rest"])
    f(respEnv["portal_web"])
    respEnv["portal_rest"] = 'A'
    respEnv["portal_web"] = 'A'
    f(respEnv["portal_rest"])
    f(respEnv["portal_web"])


def f(a):
    print(f"{a}")


if __name__ == '__main__':
    test()
