import json
import time
import socket
from flask import Flask, request, session, jsonify, make_response, send_from_directory, abort
from encryp import computePW, checkPW, createSalt
import sqlite3
from config import *
from model import User, db_init
import os
app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"

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
    print("1", request.form.__str__())
    print("2", request.values.__str__())
    print("3", request.get_data().__str__())
    print("4", request.get_json())
    username = request.values.get("username")
    password = request.values.get("password")
    print("username", username)
    print("password", password)
    if username == "" or password == "":
        code = "-1"
        data = {
            "msg": "Username or password is empty or invalid",
            "token": ""
        }
    else:
        result = User.queryByName(username)
        print(result)
        if result is None:
            code = "-1"
            data = {
                "msg": "wrong user name or password",
                "token": ""
            }
        else:
            localPW, salt = result[2], result[3]
            print("data", result)
            isConsistent = checkPW(computePW(password, salt), localPW)
            if isConsistent:
                code = "0"
                data = {
                    "msg": "Login verification succeeded",
                    "token": f"oauth.{username}"
                }
                # token = jwt.encode({"username": username}, my_secretKey, "HS256")
                # session["logintime"] = getlocaltime()
                # session["isLogin"] = True
                # session["username"] = username
                print(f"{username}用户登录成功")
            else:
                code = "-1"
                data = {
                    "msg": "wrong user name or password",
                    "token": ""
                }
                print("%s用户登录输入密码错误,登录失败" % username)

    resp = jsonify(code=code, data=data)
    # result = {"code": 200, 'data': get_host_ip()}
    return resp


@app.route('/')
def hello():
    resp = jsonify(code=200, msg=get_host_ip())
    return resp


@app.route('/getEnv', methods=["POST"])
def getEnvByToken():
    print("1", request.form.__str__())
    print("2", request.values.__str__())
    print("3", request.get_data().__str__())
    print("4", request.get_json())
    token = request.values.get("oauth_token")
    print("token", token)
    reqEnv, username = token.split(".")
    if reqEnv != "oauth":
        resp = jsonify(code=-1, data={"msg": "env error"})
        return resp
    respEnv = {
        "portal_rest": 'A',
        "portal_web": 'A',
        # "redirectUrl": "http://portal-web-a/"
        "redirectUrl": "http://127.0.0.1:8001/"
    }
    if username == "admin":
        respEnv["portal_rest"] = 'B',
        respEnv["portal_web"] = 'B',
        # respEnv["redirectUrl"] = "http://portal-web-b/"
        respEnv["redirectUrl"] = "http://127.0.0.1:8002/"
    User.generateAUTHORIZATION(username, respEnv["portal_rest"], respEnv["portal_web"])
    resp = jsonify(code=0, data={"env": respEnv})
    return resp


@app.route('/createUser', methods=["POST"])
def createUser():
    username = request.form.get("username", type=str, default="")
    password = request.form.get("password", type=str, default="")
    print(username)
    if username == "" or password == "":
        code = "-2"
        msg = "username or password null"
    else:
        user = User.queryByName(username)
        if user is not None:
            code = "-1"
            msg = "user existed"
        else:
            user = User(username, password)
            user.save()
            code = "0"
            msg = "create succeeded"
    resp = jsonify(code=code, msg=msg)
    return resp


@app.route('/getAllUserInfos', methods=["GET"])
def getAllUserInfos():
    code = "0"
    msg = json.dumps(User.all().fetchall())
    resp = jsonify(code=code, msg=msg)
    return resp


def equal(b: bytes):
    """用来补齐被JWT去掉的等号"""
    rest = len(b) % 4
    return b + '='*rest


if __name__ == '__main__':
    db_init()
    # data = jsonify(a='1', b='2')
    # print(data)
    # resp = jsonify(code=200, data=data)
    # print(resp)
    app.run(debug=True)

    # key = "secret"
    # token = jwt.encode({"test": "100"}, key, "HS256")
    # header, payload, signature = token.split(".")
    #
    # print("header=",base64.urlsafe_b64decode(equal(header)))
    # print("payout=", base64.urlsafe_b64decode(equal(payload)))
    # print("signature", base64.urlsafe_b64decode(equal(signature)))

