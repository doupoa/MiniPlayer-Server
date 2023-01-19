import base64
import config
import logging

from utils.Security import *
from utils.SQLManager import DB
from utils.Model import TokenModel, InfoModel


def get_user(username: str):
    conn = DB()
    user = conn.selectTopone(table="user", where=f"username='{username}'")
    return user


def check_user_info(data) -> TokenModel:
    if not config.AllowLogin:
        return TokenModel(status="10007")
    user = get_user(data.un)
    if not user:
        return TokenModel(status="10002")
    if not check_bcrypt(rsa_decrypt(base64.b64decode(data.pw)).encode('utf-8'), user["hash_passwd"].encode('utf-8')):
        return TokenModel(status="10003")
    return TokenModel(token=create_token(user["id"], config.ACCESS_TOKEN_EXPIRE_MINUTES), refresh_token=create_token(user["id"], config.REFRESH_TOKEN_EXPIRE_MINUTES), status='10001')


def register_user(data) -> InfoModel:
    if not config.AllowRegistration:
        return InfoModel(info="服务器关闭了注册服务", status="11007")
    conn = DB()
    user = conn.selectTopone(table="user", where=f"username='{data.un}'")
    if user:
        return InfoModel(info="用户名存在", status="11002")
    hash_pwd = bcrypt_encrypt(rsa_decrypt(
        base64.b64decode(data.pw)).encode('utf-8'))
    res = conn.insert(table="user", username=data.un, hash_passwd=hash_pwd)
    if res:
        return InfoModel(info="注册成功", status="11001")


def check_user_readonly(user_id) -> bool:
    conn = DB()
    user = conn.selectTopone(table="user",field="read_only", where=f"id='{user_id}'")
    if user == None:
        return True
    if int(user["read_only"]) == 1:
        return True
    return False