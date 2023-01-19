from datetime import datetime, timedelta
from typing import Any, Optional, Union
import config

import rsa
import bcrypt
from fastapi import FastAPI, Header
from jose import jwt

RSA_PRI_KEY = None

def create_token(
    subject: Union[str, Any], expires_delta: float = None
) -> str:
    """
    生成token
    :param subject: 保存到token的值
    :param expires_delta: 过期时间
    :return:
    """
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else: 
        expire = datetime.utcnow() + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def check_jwt_token(
     x_auth_token: Optional[str] = Header(...)
) -> Union[str, Any]:
    """
    解析验证 headers中为token的值 当然也可以用 Header(..., alias="Authentication") 或者 alias="X-token"
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(
            x_auth_token,config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        return payload
    except (jwt.JWTError, jwt.ExpiredSignatureError, AttributeError):
        # 抛出自定义异常， 然后捕获统一响应
        return None

def rsa_decrypt(data:bytes) -> str:
    # if RSA_PRI_KEY is None:
    with open('private.pem','rb') as privateFile:
        key = rsa.PrivateKey.load_pkcs1(privateFile.read())
    return rsa.decrypt(data,key).decode('utf-8')

def bcrypt_encrypt(passwd:bytes) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed.decode('utf')

def check_bcrypt(passwd:bytes,hash_passwd:bytes) -> bool:
    if bcrypt.checkpw(passwd,hash_passwd):return True
    return False
