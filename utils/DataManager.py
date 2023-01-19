from utils.SQLManager import DB
from utils.Model import InfoModel,SongInfoModel
import logging

def get_user_info(page:int,user_id:int):
    conn = DB()
    # Exclude `user_id` column
    data = conn.selectAll(table="user_data",field="id,song_url,img_url,lyric,favorited,song_name,composer",where = f"user_id='{user_id}'",limit = f"{(page-1)*10},{page*10}")
    return data

def delete_song_info(user_id:int,song_id:int) -> InfoModel:
    conn = DB()
    data = conn.delete(table='user_data',where = f'user_id={user_id} and id={song_id}')
    if data: return InfoModel(info="歌曲信息删除失败",status='13002')
    return InfoModel(info="歌曲信息删除成功",status='13003')

def change_song_info(user_id:int,item:SongInfoModel) -> InfoModel:
    conn = DB()
    if item.id == '':
        data  = conn.insert(table="user_data",user_id=user_id['sub'],song_url=item.song_url,img_url=item.img_url,lyric=item.lyric,song_name=item.song_name,composer=item.composer)
    else:
        data = conn.update(table="user_data",song_url=item.song_url,img_url=item.img_url,lyric=item.lyric,song_name=item.song_name,composer=item.composer,where=f"id='{item.id}'")
    if data: return InfoModel(info="歌曲信息添加成功",status="13004")
    return InfoModel(info="歌曲信息添加失败",status="13005")

def favorite_song(song_id:int,mode:int) -> InfoModel:
    conn = DB()
    data = conn.update(table="user_data",favorited = mode,where=f"id={song_id}")
    if data: return InfoModel(info="歌曲收藏成功",status="13006")
    return InfoModel(info="歌曲收藏失败",status="13007")