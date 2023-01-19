import logging
import uvicorn
import config

from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from utils.Model import *
from utils.Security import check_jwt_token,create_token
from utils.UserManager import check_user_info, register_user,check_user_readonly
from utils.DataManager import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=['*'],
    allow_methods=["*"],
)


@app.on_event("startup") # 启动时初始化日志配置
def startup_event():
    logging.basicConfig(level=config.LOGGING_LEVEL,format= "%(asctime)s - %(levelname)s - %(message)s",datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger("uvicorn.access")
    handler = logging.handlers.RotatingFileHandler(
        config.LOG_PATH, mode="a", maxBytes=config.LOG_SIZE, backupCount=3)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(handler)


@app.post("/login", response_model=TokenModel) # 用户登录
def login(item: LoginModel) -> any:
    return check_user_info(item)


@app.post('/register', response_model=InfoModel) # 用户注册
def register(item: RegisterModel) -> any:
    return register_user(item)


@app.get('/refresh',response_model=TokenModel) # 刷新token
def fresh_user_token(refresh = Depends(check_jwt_token)):
    if refresh == None:
        raise HTTPException(status_code=401)
    return TokenModel(token=create_token(refresh["sub"],config.ACCESS_TOKEN_EXPIRE_MINUTES),status=12001)


@app.get('/userinfo') # 获取用户歌单数据
def get_userInfo(page:Optional[int]=10,userId=Depends(check_jwt_token)):
    if userId == None:
        raise HTTPException(status_code=401)
    data = get_user_info(page,int(userId['sub']))
    return data

@app.get('/delsong',response_model=InfoModel) #删除歌曲
def delete_user_Song(song_id:int,userid=Depends(check_jwt_token)):
    if userid == None:
        raise HTTPException(status_code=401)
    if check_user_readonly(int(userid['sub'])):
        return InfoModel(info="用户只读，当前操作无效",status="13001")
    data = delete_song_info(int(userid['sub']),song_id)
    return data

@app.post('/updatesong',response_model=InfoModel) # 更新歌曲信息
def update_song(item:SongInfoModel,userid=Depends(check_jwt_token)):
    if userid == None:
        raise HTTPException(status_code=401)
    if check_user_readonly(int(userid['sub'])):
        return InfoModel(info="用户只读，当前操作无效",status="13001")
    return change_song_info(userid,item)

@app.get('/favorite',response_model=InfoModel) # 喜欢歌曲
def like_song(song_id:int,mode:int,userid=Depends(check_jwt_token)):
    if userid == None:
        raise HTTPException(status_code=401)
    if check_user_readonly(int(userid['sub'])):
        return InfoModel(info="用户只读，当前操作无效",status="13001")
    return favorite_song(song_id,mode)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
