import json
import time
import socket
from flask import Flask, request, session, jsonify, make_response, send_from_directory, abort
from encryp import computePW, checkPW, createSalt
import sqlite3
from config import *
import jwt
import base64
app = Flask(__name__)
c = None
conn = None


def get_host_ip():

    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()

    return ip


def getlocaltime():
    """格式化当前时间

    :return: 字符串格式的当前调用时间
    """
    datetime = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(time.time())).encode("utf-8")
    return datetime


# 首次Get请求下发CSRF-TOKEN
@app.route('/login', methods=["POST"])
def login():
    username = request.form.get("username", type=str, default="")
    password = request.form.get("password", type=str, default="")
    print(username)
    if username == "" or password == "":
        code = "-1"
        msg = "用户名或密码为空或不合法"
        token = ""
    else:
        result = c.execute("SELECT password, salt FROM USER WHERE USERNAME='%s'" % username).fetchone()
        if result is None:
            code = "-1"
            msg = "用户名或密码错误"
            token = ""
        else:
            localPW, salt = result[0], result[1]
            print("data", result)
            isConsistent = checkPW(computePW(password, salt), localPW)
            if isConsistent:
                code = "0"
                msg = "登录验证成功"

                # if username == "admin":

                token = jwt.encode({"username": username}, my_secretKey, "HS256")
                session["logintime"] = getlocaltime()
                session["isLogin"] = True
                session["username"] = username
                print("%s用户登录成功" % username)
            else:
                code = "-1"
                msg = "用户名或密码错误"
                token = ""
                print("%s用户登录输入密码错误,登录失败" % username)

    resp = jsonify(code=code, msg=msg, token=token)
    # result = {"code": 200, 'data': get_host_ip()}
    return resp


@app.route('/')
def hello():
    resp = jsonify(code=200, msg=get_host_ip())
    return resp


@app.route('/getEnv', methods=["GET"])
def getEnv():
    username = request.form.get("username", type=str, default="")
    oauth_rest = 'A'
    oauth_web = 'A'
    portal_rest = 'A'
    portal_web = 'A'
    redirectUrl = "http://portal-web-a/"
    if username == "admin":
        portal_rest = 'B'
        portal_web = 'B'
        redirectUrl = "http://portal-web-b/"
    data = jsonify(oauth_rest=oauth_rest, oauth_web=oauth_web, portal_rest=portal_rest, portal_web=portal_web, redirectUrl=redirectUrl)
    resp = jsonify(code=0, data=data)
    return resp


def db_init():
    global c, conn
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    print("数据库创建成功")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE USER(
    ID INT PRIMARY KEY  NOT NULL,
    USERNAME TEXT NOT NULL,
    PASSWORD TEXT NOT NULL,
    SALT TEXT NOT NULL);
    ''')
    conn.commit()
    print("用户表创建成功")


@app.route('/createUser', methods=["POST"])
def createUser():
    username = request.form.get("username", type=str, default="")
    password = request.form.get("password", type=str, default="")
    print(username)
    if username == "" or password == "":
        code = "-2"
        msg = "username or password null"
    else:
        cursor = c.execute("SELECT * FROM USER WHERE USERNAME='%s'" % (username))
        print(cursor)
        if len(cursor.fetchall()) != 0:
            code = "-1"
            msg = "user existed"
        else:
            allUserInfos = c.execute("SELECT * FROM USER")
            num = len(allUserInfos.fetchall())
            salt = createSalt()
            c.execute("INSERT INTO USER (ID,USERNAME,PASSWORD)"
                      "VALUES (%d, '%s', '%s', '%s')" % (num+1, username, computePW(password, salt), salt))
            conn.commit()
            code = "0"
            msg = "create succeeded"
    resp = jsonify(code=code, msg=msg)
    return resp


@app.route('/getAllUserInfos')
def getAllUserInfos():
    c = conn.cursor()
    allUserInfos = c.execute("SELECT * FROM USER")
    code = "0"
    msg = json.dumps(allUserInfos.fetchall())
    resp = jsonify(code=code, msg=msg)
    return resp


def equal(b: bytes):
    """用来补齐被JWT去掉的等号"""
    rest = len(b) % 4
    return b + '='*rest


if __name__ == '__main__':
    db_init()
    data = jsonify(a='1', b='2')
    print(data)
    resp = jsonify(code=200, data=data)
    print(resp)
    app.run(debug=True)
    conn.close()

    # key = "secret"
    # token = jwt.encode({"test": "100"}, key, "HS256")
    # header, payload, signature = token.split(".")
    #
    # print("header=",base64.urlsafe_b64decode(equal(header)))
    # print("payout=", base64.urlsafe_b64decode(equal(payload)))
    # print("signature", base64.urlsafe_b64decode(equal(signature)))

