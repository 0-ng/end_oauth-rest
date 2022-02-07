from hashlib import md5 as MD5
from os import urandom

def computePW(text: str, salt: str):
    """根据用户密码和数据库中的salt来计算返回md5的16进制值字符串

    :param text: 前端传来用户的密码(字符串)
    :param salt: 本地数据库存加密的盐(字符串)
    :return: 长md5后的32位16进制值字符串
    """
    s = text + salt
    m = MD5(s.encode('utf-8'))
    return m.hexdigest()


def checkPW(md5str: str, userPassword: str):
    """检查本地数据库中密码和计算后的密码是否一致

    :param md5str: 计算后的密码(字符串)
    :param userPassword: 本地的存的密码(字符串)
    :return: bool
    """
    return md5str == userPassword


def createSalt():
    """用于注册时候用户加密密码的盐

    :return: str
    """
    # return urandom(32).hex().encode('utf-8')
    return urandom(32).hex()