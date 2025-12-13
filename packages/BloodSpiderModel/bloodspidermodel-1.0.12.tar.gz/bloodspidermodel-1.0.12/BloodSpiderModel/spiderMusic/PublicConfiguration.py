class MusicPublicConfiguration:
    def __init__(self) -> None:
        pass
    

    # 返回音乐名称 + 音乐ID
    def get_music_name_and_music_id(self) -> dict:
        return {
            "name": "",
            "music_id": "",
            # "hasMv": True,
            # "mvUrl": 'https://example.com/mv/1'
        }
    
    # 获取音乐名称 + 音乐播放链接 + 音乐封面
    def get_music_name_and_music_url_and_music_cover(self) -> dict:
        return {
            "name": "",
            "music_url": "",
            "music_cover": ""
        }


    # 获取歌手名称 + 歌手介绍 + 歌手音乐列表
    def get_singer_name_and_singer_introduction_and_singer_music_list(self) -> dict:
        return {
            "artistName": "",
            "artistDesc": "",
            "singer_music_list": []
        }

    # 获取音乐播放页的数据: 歌手名称 + 歌手ID + 歌手的发布音乐总数 + 专辑名称 + 专辑ID
    def get_music_play_page_data(self) -> dict:
        return {
            "artistName": "歌手名称",
            "artistId": "歌手ID",
            "artist_music_count": "歌手的发布音乐总数",
            "albumName": "专辑名称",
            "albumId": "专辑ID"
            
        }
    
    