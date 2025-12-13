from fastmcp import FastMCP
import argparse
from .action import (
    _open_cloud_music,
    _search_and_play,
    _play_and_pause,
    _next_song,
    _pre_song,
    exe_path0
)
from .tool import (
    _hello,
    _get_song_info,
    _get_song_id,
    _lyric,
    _search_artist,
    _login_anonymous,
    _login_refresh,
    _get_artist_info,
    _get_artist_hot_songs,
    _get_music_url,
    _get_song_comment,
    _get_playlist,
    _get_toplist,
    _get_similar_songs,
    _get_style_songs,
    _start_netease_music,
    _get_uid,
    _get_user_playlist,
    _return_stylelist,
    _return_toplist_name,
    _export_playlist_html,
    _export_playlist_csv,
    _songs_recognize,
    global_cookie
)

mcp = FastMCP("MCPService")


@mcp.tool
def hello() -> dict:
    """
    version=0.1.20
    该方法无需参数
    """
    return _hello()





@mcp.tool
def get_song_info(keywords: str) -> dict:
    """
    根据关键词搜索歌曲信息
    """
    return _get_song_info(keywords)

# @mcp.tool
# def get_song_id(keywords: str) -> dict:
#     """
#     根据关键词搜索歌曲，返回第一首歌的ID
#     :param keywords: 歌曲关键词
#     :return: 歌曲ID
#     """
#     return _get_song_id(keywords)

@mcp.tool
def lyric(keywords: str) -> dict:
    """
    根据歌名关键词搜索歌词
    """
    return _lyric(keywords)

@mcp.tool
def get_music_url(keywords: str, level: str = "standard") -> dict:
    """
    根据关键词获取音乐在线试听url
    """
    return _get_music_url(keywords, level)

@mcp.tool
def get_song_comment(keywords: str) -> dict:
    """
    根据歌名关键词获取歌曲评论
    """
    return _get_song_comment(keywords)

@mcp.tool
def get_similar_songs(keywords: str) -> dict:
    """
    根据关键词获取相似音乐
    """
    return _get_similar_songs(keywords)

@mcp.tool
def get_style_songs(style_name: str) -> dict:
    """
    根据曲风名返回歌曲列表。允许查询的曲风可以调用 return_stylelist 获取参考。
    """
    return _get_style_songs(style_name)





@mcp.tool
def search_artist(keyword: str) -> dict:
    """
    根据关键词搜索歌手简要信息
    """
    return _search_artist(keyword)

@mcp.tool
def get_artist_info(keyword: str) -> dict:
    """
    根据关键词获取歌手详细信息
    """
    return _get_artist_info(keyword)

@mcp.tool
def get_artist_hot_songs(keyword: str) -> dict:
    """
    根据关键词获取歌手最火的50首歌曲
    """
    return _get_artist_hot_songs(keyword)





@mcp.tool
def get_playlist(id: str) -> dict:
    """
    根据歌单id获取歌单详情
    """
    return _get_playlist(id)

@mcp.tool
def get_toplist(name: str) -> dict:
    """
    根据排行榜名字获取榜单详情。支持查询排行榜可以调用return_toplist_name获取参考。
    """
    return _get_toplist(name)





# @mcp.tool()
# def get_uid(nickname: str) -> dict:
#     """
#     根据用户昵称获取其uid
#     :param nickname: 用户昵称
#     :return: 用户uid json
#     """
#     return _get_uid(nickname)

@mcp.tool()
def get_user_playlist(nickname: str) -> dict:
    """
    输入用户昵称，获取用户歌单（含有歌单id）
    """
    return _get_user_playlist(nickname)





@mcp.tool
def return_stylelist() -> dict:
    """
    返回所有风格名称，获取所有歌曲风格
    该方法无需参数
    """
    return _return_stylelist()

@mcp.tool
def return_toplist_name() -> dict:
    """
    返回所有排行榜名称
    该方法无需参数
    """
    return _return_toplist_name()

@mcp.tool
def export_playlist_html(id: str, path: str = None) -> dict:
    """
    根据歌单id生成精美HTML，path不为None则保存到相应文件路径，否则直接返回html字符串。
    文件路径应该类似C:\\Users\\Ben\\Desktop\\playlist.html
    """
    try:
        result = _export_playlist_html(id, path)
        return {"code": 200, "msg": "success", "data": result}
    except Exception as e:
        return {"code": 500, "msg": f"生成歌单HTML失败: {e}", "data": ""}


@mcp.tool
def export_playlist_csv(id: str, path: str = None) -> dict:
    """
    根据歌单id导出为CSV，path不为None则保存到文件，否则直接返回csv字符串
    文件路径应该类似C:\\Users\\Ben\\Desktop\\playlist.csv
    """
    try:
        result = _export_playlist_csv(id, path)
        return {"code": 200, "msg": "success", "data": result}
    except Exception as e:
        return {"code": 500, "msg": f"导出歌单CSV失败: {e}", "data": ""}


# @mcp.tool
# def login_anonymous() -> dict:
#     """
#     游客登录，获取游客 cookie，并保存到全局变量
#     :return: 游客 cookie 字符串
#     """
#     return _login_anonymous()

# @mcp.tool
# def login_refresh() -> dict:
#     """
#     刷新登录状态，获取新的 cookie
#     :return: 新的 cookie 字符串
#     """
#     return _login_refresh()


# @mcp.tool()
# def start_netease_music(exe_path: str) -> dict:
#     """
#     启动本地网易云音乐客户端
#     :param exe_path: 网易云音乐客户端的 exe 路径，默认 C:\\CloudMusic\\cloudmusic.exe
#     :return: 启动结果 json
#     """
#     return _start_netease_music(exe_path)

@mcp.tool()
def open_cloud_music(exe_path: str = None) -> dict:
    """
    启动本地网易云音乐客户端。此方法仅支持本地调用。
    :param exe_path: 网易云音乐的 exe 路径
    """
    return _open_cloud_music(exe_path)

@mcp.tool()
def search_and_play_mcp(keyword: str) -> dict:
    """
    搜索并播放指定歌曲。此方法仅支持本地调用。
    建议先调用open_cloud_music打开网易云客户端。
    """
    return _search_and_play(keyword)

@mcp.tool()
def play_and_pause_mcp() -> dict:
    """
    播放/暂停当前歌曲。此方法仅支持本地调用。
    该方法无需参数
    """
    return _play_and_pause()

@mcp.tool()
def next_song() -> dict:
    """
    切换到下一首歌曲。此方法仅支持本地调用。
    该方法无需参数
    """
    return _next_song()

@mcp.tool()
def pre_song() -> dict:
    """
    切换到上一首歌曲。此方法仅支持本地调用。
    该方法无需参数
    """
    return _pre_song()


@mcp.tool
def songs_recognize(audio_path: str, api_key: str) -> dict:
    """
    听歌识曲。此方法仅支持本地调用。
    :param audio_path: 本地音频文件路径。建议不要超过20秒。
    :param api_key: RapidAPI key，(https://rapidapi.com/tipsters/api/shazam-core)
    """
    return _songs_recognize(audio_path, api_key)

def main():
    parser = argparse.ArgumentParser(description="启动 ben-music-mcp 服务")
    parser.add_argument('--transport', type=str, default="stdio", choices=["stdio", "sse"], help="传输方式")
    args = parser.parse_args()
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    # mcp.run(transport="sse")
    main()