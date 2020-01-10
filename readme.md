一.网易云音乐下载  
1.单首歌曲下载  
2.整个歌单下载  
3.vip收费歌曲下载(只有vip能听的不可以下载)  
4.歌词下载

二.思路：  
1.抓包定位到资源的链接  
2.根据资源链接找到获取MP3所需的参数
3.根据参数和api接口定位到加密的js代码  
4.用charles hook js代码找出js加密代码中的固定参数。用python实现加密代码部分  
5.根据歌的id进行下载保存  
6.解析歌单批量下载 

三.用法  
1.单首歌曲  
    get_song_by_sid('436514312')  
    436514312 为歌曲id
2.歌单下载   
    url = https://music.163.com/playlist?id=27545272  
    download_playlist(url,multi=6)    
    歌单url地址和下载线程数