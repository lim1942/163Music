import os
import re
import json
import traceback

import requests
from concurrent.futures import ThreadPoolExecutor,as_completed

from aes import  MyCrypto

IV = "0102030405060708"
MY_CRYPTO = MyCrypto()
HEADERS = {
'Connection': 'keep-alive',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',}

def get_post_data(info):
    """加密参数"""
    key_first = "0CoJUm6Qyw8W8jud"
    first = MY_CRYPTO.encrypt(key_first,IV,json.dumps(info).replace(' ', ''))
    key_second = "KHM4GhhSJFakMyn2"
    second = MY_CRYPTO.encrypt(key_second,IV,first)
    post_data = {"params": second,
    'encSecKey': '8c1685c5ab2e5a22c86505ca56ac860ae5415d3ecc37837e3c947e80c7d2604f36a'
      '755ad2c5f1f8d0f5f044cd4a60d2212e665aa3d6e747216a96f682aec522789b08a06f14a1d0b2'
      '6528b67def65abee7e7de475100b903acb63c40f06f74766f59cca16801a32affb6d647180fe1e3'
      'f78b7d13ffd96369d3671d10a4632684'}
    return post_data

def download_lyric(sid,dir_name,name):
    """下载歌词"""
    url = f"http://music.163.com/api/song/lyric?id={sid}&lv=1&kv=1&tv=-1"
    lyric_content = requests.get(url,headers=HEADERS).content
    lyric_path = os.sep.join([dir_name,'lyrics'])
    if not os.path.exists(lyric_path):os.mkdir(lyric_path)
    lyric_item_path = os.path.join(lyric_path,name+'.lrc')
    with open(lyric_item_path,'wb') as f:f.write(lyric_content)

def get_song_by_sid(sid,dir_name,name=None):
    """根据一首歌的id采集"""
    try:
        print(f"start {sid} -- {name}")
        name = name.replace(os.sep,'-')
        if not os.path.exists(dir_name):os.mkdir(dir_name)
        song_path = os.path.join(dir_name,(name or sid)+'.mp3')
        # 已经存在不再下载
        if os.path.exists(song_path):
            print(f'{sid} -- {song_path} already download !!!')
            return sid
        # 获取音乐的下载地址
        url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
        info = {"ids": f"[{sid}]", "level": "standard", "encodeType": "aac", "csrf_token": ""}
        data = get_post_data(info)
        song_json_resp = requests.post(url,data=data,headers=HEADERS)
        song_json = song_json_resp.json()
        song_url = song_json['data'][0]['url']
        assert 'http' in song_url, "this song need vip !!!"
        # 进行音乐下载
        song_resp = requests.get(song_url,headers=HEADERS)
        with open(song_path,'wb') as f:f.write(song_resp.content)
        # 下载音乐的歌词
        download_lyric(sid, dir_name, name)
        print(f'{sid} -- {song_path} finish !!!')
        return sid
    except:
        print(f"{sid} -- {name} : {traceback.format_exc()}")


def download_playlist(url,multi=0):
    """采集网易云歌单，输入歌单地址"""
    # 采集歌单数据
    resp = requests.get(url,headers=HEADERS)
    playlist_name = re.search("<title>(.*?) - 歌单 - 网易云音乐",resp.text).groups()[0].strip().replace(os.sep,'-')
    songs = re.findall('<a href="/song\?id=(\d+?)">(.+?)</a>',resp.text)
    songs = dict(songs)
    print(f"所有的歌曲如下 {len(songs)} 首...\n")
    print(list(songs.values()))
    # 单线程采集歌曲
    if not multi:
        for sid,name in songs.items():
            key = get_song_by_sid(sid,playlist_name,name)
            if key: del songs[key]
    # 多线程采集歌曲
    else:
        pool = ThreadPoolExecutor(multi)
        tasks = [pool.submit(get_song_by_sid,sid,playlist_name,name) for sid,name in songs.items()]
        for future in as_completed(tasks):
            key = future._result
            if key: del songs[key]
    print(f"\n没完成下载的歌曲如下 {len(songs)} 首...")
    print(list(songs.values()))


if __name__ == "__main__":
    # 单首歌曲按id下载
    # get_song_by_sid('436514312')
    # 歌单地址：
    url = "https://music.163.com/playlist?id=27545272"
    download_playlist( url ,multi=6)