from pydantic import BaseModel


class LoginModel(BaseModel):
    un: str = None
    pw: str = None


class RegisterModel(BaseModel):
    un: str = None
    pw: str = None


class TokenModel(BaseModel):
    token: str = None
    refresh_token: str = None
    status: str = None


class InfoModel(BaseModel):
    info: str = None
    status: str = None

class SongInfoModel(BaseModel):
    id: str = None
    song_name: str = None
    composer: str = None
    song_url: str = None
    lyric: str = None
    img_url: str = None
