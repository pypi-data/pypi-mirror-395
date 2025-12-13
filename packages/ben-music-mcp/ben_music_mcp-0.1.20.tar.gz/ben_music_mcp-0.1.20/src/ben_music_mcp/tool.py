

import subprocess
import requests

# 全局变量保存 cookie
global_cookie = {}

import os
import json
from urllib.parse import quote
import concurrent.futures
from .html_template import generate_playlist_html

# base_url = "https://ncm.nekogan.com"
# base_url = "https://ben-cloud-music-project.vercel.app"
base_url = "https://www.megumi-ben.cn"
base_urls = [
    "https://www.megumi-ben.cn",
    "https://ben-cloud-music-project.vercel.app",
    # "https://www.megumi-ben.cn2"
]

def _save_cookie_to_file(cookie: dict, filename: str = "cookie.txt"):
    """将cookie保存到文件"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(cookie, ensure_ascii=False))

def _load_cookie_from_file(filename: str = "cookie.txt") -> dict:
    """从文件读取cookie"""
    if not os.path.exists(filename):
        # 这里直接返回你的硬编码cookie
        return {
            "MUSIC_A_T": "1762674143805",
            "MUSIC_R_T": "0",
            "MUSIC_A": "00FD2909A8CC993C4FB0FC90128C7E2E3EEC34146238C0F67438D16B51DB026C9AC74700E4270BCF0954B0454EDA13126BBD915DF4CF52EF21ACB5141059BEFA897B59C94F25484D47A8C8B257C322CB9D745805D39E61449D59DF795D936D9F5F628CE6E0D6610792EB91B0D34EBFB837357B9AC0135C97B18B1D6FB1EA248B5532FEFF6A34A5C57B4EDE76C36AACF86A542A7358C44E0F2978A3B7AA852F2A84DA48857A5CAAE3FA2D4968232C727BFD96CD7D7E7479829C726EC940B1880EFD01740C665B517699FAAEF1CA3BDD92E049A36AB793A15AD9AD75E4D691D4D821E363CAE7BF3AC9586A653999810747C974239EC1E43944EB679B3DC92CFF113BDBC9279CCDCD5271C55DD18FE58847F6AF6D5E12D1D8BB8417D99B2AEDF13B4EC9097EE893ABD6BBC56E37187D2386D061DE4288B289AD7F4068E488B691682F61F170D1DDB0E6D84A679E49677A1E529C96FE9540E0B5527B1D23C956FEAB3CB6B3647B749B1CAE39EE70CC6FFC06E5F4AC33DA9470E856C1391FD7006FB487C9537E4D11B2D469A78615B32771CAE5A725D8FD8FA172E865A236F487B665817AE5F57F4AF8781F2663CA0E5780CBBF4474D616D068125C6EAFC1741C5B844F8BB6621037BA47FC0CD9E48FA63499730DF294E62E3A2CF99319D6DD778B573CCB7B99B2AFC4CC9035540E3864862E2707B4898BD831AF07C4F0774ED9AFA3F96B94079C3F48D262C4898BD0A3E39016",
            "__csrf": "eabbb81b921eb9637c0b389245b3a0dc",
            "MUSIC_R_U": "00F9CF8A93CB06AEC0A041DB4FC98922D18884F91B648A3F78CC43943902835DB940DC984AC33ED14A019B44DCDB707C2FA8F2ED50EC556FB93B675A320C20F5E39A3EA15488819D77A922244FB3B663B4"
        }
        # return {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.loads(f.read())
    except Exception:
        return {}

def _get_cookie() -> dict:
    """获取当前cookie（优先文件）"""
    global global_cookie
    if global_cookie:
        return global_cookie
    cookie = _load_cookie_from_file()
    global_cookie = cookie
    return cookie

def _hello() -> dict:
    """方法注释"""
    return {"code": 200, "msg": "success", "data": "你好世界"}




def multi_base_get(path, **kwargs):
    """
    并发请求多个 base_url + path，谁先返回有效响应就返回谁
    :param base_urls: 基础 url 列表
    :param path: 路径和查询部分（如 "/search?keywords=xxx&randomCNIP=true"）
    :param kwargs: 其它 requests.get 参数（如 timeout、cookies 等）
    :return: 第一个成功的 requests.Response 对象，全部失败则返回 None
    """
    def fetch(base_url):
        url = base_url.rstrip("/") + path
        try:
            resp = requests.get(url, **kwargs)
            resp.raise_for_status()
            return resp
        except Exception:
            return None

    # with concurrent.futures.ThreadPoolExecutor(max_workers=len(base_urls)) as executor:
    #     futures = [executor.submit(fetch, base_url) for base_url in base_urls]
    #     for future in concurrent.futures.as_completed(futures):
    #         result = future.result()
    #         if result:
    #             return result
    for base_url in base_urls:
        try:
            return fetch(base_url)
        except Exception:
            continue
    return None
def _get_song_info(keywords: str) -> dict:
    """
    搜索歌曲，返回json格式
    :param keywords: 歌曲关键词
    :return: 歌曲信息json
    """
    encoded_keywords = quote(keywords)
    # encoded_keywords = keywords
    # url = f"{base_url}/search?keywords={encoded_keywords}&randomCNIP=true"
    ext_path = f"/search?keywords={encoded_keywords}&randomCNIP=true"
    try:
        # resp = requests.get(url, timeout=15)
        # resp.raise_for_status()
        resp=multi_base_get(ext_path,timeout=15)
        data = resp.json()
        if "result" in data and "songs" in data["result"]:
            songs = data["result"]["songs"]
            if not songs:
                return {"code": 404, "msg": "未找到相关歌曲", "data": {}}
            song = songs[0]
            return {
                "code": 200,
                "msg": "success",
                # "keywords": keywords,
                # "query": encoded_keywords,
                "data": {
                    "id": song.get("id", "未知"),
                    "name": song.get("name", "未知"),
                    "artists": [a["name"] for a in song.get("artists", [])],
                    "album": song.get("album", {}).get("name", "未知"),
                    "alias": song.get("alias", []),
                    "transNames": song.get("transNames", []),
                    "duration": song.get("duration", 0),
                    "fee": song.get("fee", 0),
                    "mvid": song.get("mvid", 0)
                }
            }
        else:
            return {"code": 404, "msg": "未找到相关歌曲", "data": {}}
    except Exception as e:
        return {"code": 500, "msg": f"请求失败: {e}", "data": {}}

def _get_song_id(keywords: str) -> dict:
    """
    搜索歌曲，返回第一个歌曲ID，json格式
    :param keywords: 歌曲关键词
    :return: 歌曲ID json
    """
    result = _get_song_info(keywords)
    if result.get("code") == 200 and "id" in result.get("data", {}):
        return {"code": 200, "msg": "success", "id": str(result["data"]["id"])}
    return {"code": 404, "msg": "未找到相关歌曲ID", "id": ""}

def _lyric(keywords: str) -> dict:
    """先获取歌曲id，再查歌词，返回json"""
    song_id_json = _get_song_id(keywords)
    song_id = song_id_json.get("id", "")
    if not song_id or not song_id.isdigit():
        return {"code": 404, "msg": f"未找到歌曲ID，原因：{song_id_json}", "data": ""}
    ext_path = f"/lyric?id={song_id}&randomCNIP=true"
    try:
        resp = multi_base_get(ext_path, timeout=15)
        data = resp.json()
        lyric_text = data.get("lrc", {}).get("lyric", "")
        if lyric_text:
            return {"code": 200, "msg": "success", "data": lyric_text}
        else:
            return {"code": 404, "msg": "未找到歌词。", "data": ""}
    except Exception as e:
        return {"code": 500, "msg": f"请求失败 {e}", "data": ""}


def _search_artist(keyword: str) -> dict:
    """
    搜索歌手，返回json格式
    :param keyword: 歌手关键词
    :return: 歌手信息json
    """
    ext_path = f"/ugc/artist/search?keyword={keyword}&randomCNIP=true"
    try:
        cookie = _get_cookie()
        resp = multi_base_get(ext_path, timeout=15, cookies=cookie)
        data = resp.json()
        data_field = data.get("data")
        if not data_field or "list" not in data_field:
            return {"code": 404, "msg": "未找到相关歌手", "data": {}}
        artists = data_field.get("list", [])
        if not artists:
            return {"code": 404, "msg": "未找到相关歌手", "data": {}}
        artist = artists[0]
        return {
            "code": 200,
            "msg": "success",
            "data": {
                "artistName": artist.get("artistName", "未知"),
                "artistId": artist.get("artistId", "未知"),
                "avatar": artist.get("artistAvatarPicUrl", "")
            }
        }
    except Exception as e:
        return {"code": 500, "msg": f"请求失败: {e}", "data": {}}

def _get_artist_id(keyword: str) -> dict:
    """
    根据关键词搜索歌手，返回第一个歌手ID，json格式
    :param keyword: 歌手关键词
    :return: 歌手ID json
    """
    # 优先从artists.json查找artist_id
    try:
        artists_path = os.path.join(os.path.dirname(__file__), "artists.json")
        with open(artists_path, "r", encoding="utf-8") as f:
            artists_list = json.load(f)
        for item in artists_list:
            if any(keyword.lower() == name.lower() for name in item.get("names", [])):
                artist_id = str(item.get("artist_id", ""))
                if artist_id.isdigit():
                    print("成功")
                    return {"code": 200, "msg": "success", "id": artist_id}
    except Exception:
        return {"code": 404, "msg": "未找到相关歌手ID", "id": ""}
    # 查不到再走API
    result = _search_artist(keyword)
    if result.get("code") == 200 and "artistId" in result.get("data", {}):
        return {"code": 200, "msg": "success", "id": str(result["data"]["artistId"])}
    return {"code": 404, "msg": "未找到相关歌手ID", "id": ""}


def _get_artist_info(keyword: str) -> dict:
    """
    根据关键词获取歌手详细信息，先查id再查详情，返回json
    :param keyword: 歌手关键词
    :return: 歌手详细信息json
    """
    id_json = _get_artist_id(keyword)
    artist_id = id_json.get("id", "")
    if not artist_id or not artist_id.isdigit():
        return {"code": 404, "msg": f"未找到歌手ID，原因：{id_json}", "data": {}}
    ext_path = f"/ugc/artist/get?id={artist_id}&randomCNIP=true"
    try:
        cookie = _get_cookie()
        resp = multi_base_get(ext_path, timeout=15, cookies=cookie)
        data = resp.json()
        return {"code": 200, "msg": "success", "data": data}
    except Exception as e:
        return {"code": 500, "msg": f"请求失败: {e}", "data": {}}

def _get_artist_hot_songs(keyword: str) -> dict:
    """
    根据关键词获取歌手最火的50首歌曲，先查id再查热门歌曲，返回json
    :param keyword: 歌手关键词
    :return: 热门歌曲json
    """
    # 优先从artists.json查找artist_id
    id_json = _get_artist_id(keyword)
    artist_id = id_json.get("id", "")
    if not artist_id or not artist_id.isdigit():
        return {"code": 404, "msg": f"未找到歌手ID，原因：{id_json}", "data": []}
    ext_path = f"/artist/top/song?id={artist_id}&randomCNIP=true"
    try:
        cookie = _get_cookie()
        resp = multi_base_get(ext_path, timeout=15, cookies=cookie)
        data = resp.json()
        return {"code": 200, "msg": "success", "data": data}
    except Exception as e:
        return {"code": 500, "msg": f"请求失败: {e}", "data": []}


def _get_music_url(keywords: str, level: str = "standard") -> dict:
    """
    根据关键词获取音乐播放url，先查歌曲id再查url，返回json
    :param keywords: 歌曲关键词
    :param level: 音质等级
    :return: 音乐url json
    """
    id_json = _get_song_id(keywords)
    song_id = id_json.get("id", "")
    if not song_id or not song_id.isdigit():
        return {"code": 404, "msg": f"未找到歌曲ID，原因：{id_json}", "data": {}}
    # url = f"{base_url}/song/url/v1?id={song_id}&level={level}&randomCNIP=true&unblock=true"
    url = f"https://music-api.gdstudio.xyz/api.php?types=url&source=netease&id={song_id}&br=128"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return {"code": 200, "msg": "success", "data": data.get("url", "无")}
    except Exception as e:
        return {"code": 500, "msg": f"请求失败: {e}", "data": {}}


def _get_song_comment(keywords: str) -> dict:
    """
    根据关键词获取歌曲评论，只保留有用信息，返回json
    :param keywords: 歌曲关键词
    :return: 歌曲评论json
    """
    id_json = _get_song_id(keywords)
    song_id = id_json.get("id", "")
    if not song_id or not song_id.isdigit():
        return {"code": 404, "msg": f"未找到歌曲ID，原因：{id_json}", "data": []}
    # url = f"{base_url}/comment/music?id={song_id}&randomCNIP=true"
    ext_path=f"/comment/music?id={song_id}&randomCNIP=true"
    try:
        # resp = requests.get(url, timeout=15)
        # resp.raise_for_status()
        resp=multi_base_get(ext_path,timeout=15)
        # resp.raise_for_status())
        data = resp.json()
        hot_comments = data.get("hotComments", [])
        # 只保留有用字段
        result = []
        for c in hot_comments:
            user = c.get("user", {})
            result.append({
                "nickname": user.get("nickname", "未知"),
                "content": c.get("content", ""),
                "likedCount": c.get("likedCount", 0),
                "timeStr": c.get("timeStr", "")
            })
        return {"code": 200, "msg": "success", "data": result}
    except Exception as e:
        return {"code": 500, "msg": f"请求失败: {e}", "data": []}


def _get_playlist(id):
    """
    获取歌单详情，只返回关键字段。
    参数: id (歌单id)
    返回: JSON
    """
    ext_path = f"/playlist/detail?id={id}&randomCNIP=true"
    try:
        resp = multi_base_get(ext_path, timeout=15)
        data = resp.json()
        if data.get("code") != 200 or "playlist" not in data:
            return {"code": 500, "msg": "请求失败"}
        pl = data["playlist"]
        result = {
            "id": pl.get("id"),
            "name": pl.get("name"),
            "coverImgUrl": pl.get("coverImgUrl"),
            "userId": pl.get("userId"),
            "createTime": pl.get("createTime"),
            "trackCount": pl.get("trackCount"),
            "playCount": pl.get("playCount"),
            "subscribedCount": pl.get("subscribedCount"),
            "description": pl.get("description"),
            "tags": pl.get("tags", []),
            "tracks": []
        }
        for t in pl.get("tracks", []):
            track = {
                "id": t.get("id"),
                "name": t.get("name"),
                "ar": [a.get("name") for a in t.get("ar", [])],
                "al": t.get("al", {}).get("name"),
                "alia": t.get("alia", [])
            }
            result["tracks"].append(track)
        return result
    except Exception as e:
        return {"code": 500, "msg": str(e)}


def _get_toplist(name: str) -> dict:
    """
    根据排行榜名获取榜单详情（先查id再查_get_playlist）
    :param name: 榜单名称
    :return: 榜单详情json
    """
    try:
        path = os.path.join(os.path.dirname(__file__), "toplist.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        toplists = data.get("toplists", [])
        match = next((item for item in toplists if item.get("name") == name), None)
        if not match:
            return {"code": 404, "msg": f"未找到榜单: {name}"}
        # 这里直接调用 _get_playlist，已自动并发主备url
        return _get_playlist(match["id"])
    except Exception as e:
        return {"code": 500, "msg": f"读取榜单失败: {e}"}


def _get_similar_songs(keywords: str) -> dict:
    """
    根据关键词获取相似音乐（先查id再查/simi/song）
    :param keywords: 歌曲关键词
    :return: 相似音乐json
    """
    id_json = _get_song_id(keywords)
    song_id = id_json.get("id", "")
    if not song_id or not song_id.isdigit():
        return {"code": 404, "msg": f"未找到歌曲ID，原因：{id_json}", "data": []}
    # url = f"{base_url}/simi/song?id={song_id}&randomCNIP=true"
    ext_path = f"/simi/song?id={song_id}&randomCNIP=true"
    try:
        # resp = requests.get(url, timeout=15)
        # resp.raise_for_status()
        resp=multi_base_get(ext_path,timeout=15)
        data = resp.json()
        songs = data.get("songs", [])
        result = []
        for s in songs:
            result.append({
                "id": s.get("id"),
                "name": s.get("name"),
                "artists": [a.get("name") for a in s.get("artists", [])],
                "album": s.get("album", {}).get("name"),
                "duration": s.get("duration")
            })
        return {"code": 200, "msg": "success", "data": result}
    except Exception as e:
        return {"code": 500, "msg": f"请求失败: {e}", "data": []}


def _get_style_songs(style_name: str) -> dict:
    """
    根据曲风名获取对应曲风id，再查 /style/song?tagId=xxx，返回歌曲列表。
    :param style_name: 曲风名
    :return: 歌曲列表json
    """

    # 读取 styleList.json
    try:
        path = os.path.join(os.path.dirname(__file__), "styleList.json")
        with open(path, "r", encoding="utf-8") as f:
            style_list = json.load(f)
    except Exception as e:
        return {"code": 500, "msg": f"读取曲风列表失败: {e}", "data": {}}

    tag_id = None
    for item in style_list:
        if item.get("tagName") == style_name:
            tag_id = item.get("tagId")
            break
    if not tag_id:
        return {"code": 404, "msg": f"未找到曲风: {style_name}", "data": {}}

    ext_path = f"/style/song?tagId={tag_id}&randomCNIP=true"
    try:
        cookie = _get_cookie()
        resp = multi_base_get(ext_path, timeout=15, cookies=cookie)
        data = resp.json()
        page = data.get("page", {})
        songs = data.get("songs")
        # 自动适配嵌套结构
        if songs is None:
            for v in data.values():
                if isinstance(v, dict) and "songs" in v:
                    songs = v["songs"]
                    break
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict) and "songs" in item:
                            songs = item["songs"]
                            break
        if songs is None:
            songs = []
        # 只保留关键信息
        result = []
        for s in songs:
            if isinstance(s, dict):
                result.append({
                    "id": s.get("id"),
                    "name": s.get("name"),
                    "artists": [a.get("name") for a in s.get("ar", [])],
                    "album": s.get("al", {}).get("name"),
                    "duration": s.get("dt")
                })
        return {"code": 200, "msg": "success", "data": result}
    except Exception as e:
        return {"code": 500, "msg": f"请求失败: {e}", "data": {}}



def _get_uid(nickname: str) -> dict:
    """
    根据用户昵称获取其uid
    :param nickname: 用户昵称
    :return: 用户uid json
    """
    encoded_nickname = quote(nickname)
    ext_path = f"/get/userids?nicknames={encoded_nickname}&randomCNIP=true"
    try:
        resp = multi_base_get(ext_path, timeout=15)
        data = resp.json()
        # 适配 nicknames 字段结构
        nick_dict = data.get("nicknames", {})
        if not nick_dict:
            return {"code": 404, "msg": "未找到用户", "data": {}}
        # 取第一个昵称和uid
        for n, uid in nick_dict.items():
            return {"code": 200, "msg": "success", "data": {"uid": uid, "nickname": n}}
        return {"code": 404, "msg": "未找到用户", "data": {}}
    except Exception as e:
        return {"code": 500, "msg": f"请求失败: {e}", "data": {}}

def _get_user_playlist(nickname: str) -> dict:
    """
    输入用户昵称，获取用户歌单（只保留必要字段）
    :param nickname: 用户昵称
    :return: 歌单列表json
    """
    # 第一步：获取uid
    uid_result = _get_uid(nickname)
    if uid_result.get("code") != 200 or "uid" not in uid_result.get("data", {}):
        return {"code": 404, "msg": f"未找到用户: {nickname}", "data": []}
    uid = uid_result["data"]["uid"]
    # 第二步：获取歌单
    ext_path = f"/user/playlist?uid={uid}&randomCNIP=true"
    try:
        resp = multi_base_get(ext_path, timeout=15)
        data = resp.json()
        playlists = data.get("playlist", [])
        result = []
        for pl in playlists:
            result.append({
                "id": pl.get("id"),
                "name": pl.get("name"),
                "coverImgUrl": pl.get("coverImgUrl"),
                "trackCount": pl.get("trackCount"),
                "playCount": pl.get("playCount"),
                "creator": {
                    "userId": pl.get("creator", {}).get("userId"),
                    "nickname": pl.get("creator", {}).get("nickname"),
                    "avatarUrl": pl.get("creator", {}).get("avatarUrl")
                }
            })
        return {"code": 200, "msg": "success", "data": result}
    except Exception as e:
        return {"code": 500, "msg": f"请求失败: {e}", "data": []}


def _return_stylelist() -> dict:
    """
    返回所有风格名称（不含id），从styleList.json读取。
    :return: {"code": 200, "msg": "success", "data": [风格名列表]}
    """
    try:
        path = os.path.join(os.path.dirname(__file__), "styleList.json")
        with open(path, "r", encoding="utf-8") as f:
            style_list = json.load(f)
        names = [item.get("tagName", "") for item in style_list if item.get("tagName")]
        return {"code": 200, "msg": "success", "data": names}
    except Exception as e:
        return {"code": 500, "msg": f"读取风格列表失败: {e}", "data": []}


def _return_toplist_name() -> dict:
    """
    返回所有排行榜名称（不含id），从toplist.json读取。
    :return: {"code": 200, "msg": "success", "data": [榜单名列表]}
    """
    try:
        path = os.path.join(os.path.dirname(__file__), "toplist.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        toplists = data.get("toplists", [])
        names = [item.get("name", "") for item in toplists if item.get("name")]
        return {"code": 200, "msg": "success", "data": names}
    except Exception as e:
        return {"code": 500, "msg": f"读取榜单列表失败: {e}", "data": []}


def _export_playlist_html(id: str, path: str = None) -> str:
    """
    根据歌单id生成精美HTML，path不为None则保存到文件，否则直接返回html字符串
    注意：如果输入路径，需要包含文件名，例如C:\\Users\\Ben\\Desktop\\playlist.html而不是C:\\Users\\Ben\\Desktop
    :param id: 歌单id
    :param path: 保存路径，默认None
    :return: html字符串或保存结果
    """
    playlist = _get_playlist(id)
    html = generate_playlist_html(playlist, base_url)
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return f"已保存到 {path}"
    return html

def _export_playlist_csv(id: str, path: str = None) -> str:
    """
    根据歌单id导出为CSV，path不为None则保存到文件，否则直接返回csv字符串
    :param id: 歌单id
    :param path: 保存路径，默认None
    :return: csv字符串或保存结果
    """
    import csv
    import io
    playlist = _get_playlist(id)
    if not isinstance(playlist, dict) or "tracks" not in playlist:
        return "歌单信息获取失败"
    output = io.StringIO()
    writer = csv.writer(output)
    # 写表头
    writer.writerow(["序号", "歌曲ID", "歌名", "歌手", "专辑", "别名"])
    for idx, track in enumerate(playlist["tracks"], 1):
        writer.writerow([
            idx,
            track.get("id", ""),
            track.get("name", ""),
            ", ".join(track.get("ar", [])),
            track.get("al", ""),
            ", ".join(track.get("alia", []))
        ])
    csv_str = output.getvalue()
    output.close()
    if path:
        with open(path, "w", encoding="utf-8", newline='') as f:
            f.write(csv_str)
        return f"已保存到 {path}"
    return csv_str
    



def _login_anonymous() -> dict:
    url = f"{base_url}/register/anonimous?randomCNIP=true"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        cookie = resp.cookies.get_dict()
        global global_cookie
        global_cookie = cookie
        _save_cookie_to_file(cookie)
        return {"code": 200, "msg": "游客登录成功", "cookie": cookie, "data": data}
    except Exception as e:
        return {"code": 500, "msg": f"游客登录失败: {e}", "cookie": {}, "data": {}}

def _login_refresh() -> dict:
    url = f"{base_url}/login/refresh?randomCNIP=true"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        cookie = resp.cookies.get_dict()
        return {"code": 200, "msg": "登录状态刷新成功", "cookie": cookie, "data": data}
    except Exception as e:
        return {"code": 500, "msg": f"刷新登录失败: {e}", "cookie": {}, "data": {}}


def _start_netease_music(exe_path: str) -> dict:
    """
    启动本地网易云音乐客户端
    :param exe_path: 网易云音乐客户端的 exe 路径
    :return: 启动结果 json
    """
    try:
        subprocess.Popen(exe_path)
        return {"code": 200, "msg": "网易云音乐已启动", "exe_path": exe_path}
    except Exception as e:
        return {"code": 500, "msg": f"启动失败: {e}", "exe_path": exe_path}



def _songs_recognize(audio_path: str, api_key: str) -> dict:
    """
    识别音频文件中的歌曲，返回关键信息。
    :param audio_path: 本地音频文件路径
    :param api_key: RapidAPI key
    :return: dict {code, msg, data}
    """
    import requests
    url = "https://shazam-core.p.rapidapi.com/v1/tracks/recognize"
    try:
        files = {
            "file": (audio_path.split("\\")[-1], open(audio_path, "rb"), "audio/mpeg")
        }
        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "shazam-core.p.rapidapi.com"
        }
        response = requests.post(url, files=files, headers=headers)
        data = response.json()
        track = data.get('track', {})
        title = track.get('title', '')
        artist = track.get('subtitle', '')
        album = ''
        for section in track.get('sections', []):
            if section.get('type') == 'SONG':
                for meta in section.get('metadata', []):
                    if meta.get('title') == 'Album':
                        album = meta.get('text', '')
        cover = track.get('images', {}).get('coverart', '')
        shazam_url = track.get('url', '')
        result = {
            "title": title,
            "artist": artist,
            "album": album,
            "cover": cover,
            "shazam_url": shazam_url
        }
        if title:
            return {"code": 200, "msg": "success", "data": result}
        else:
            return {"code": 404, "msg": "未识别到歌曲", "data": {}}
    except Exception as e:
        return {"code": 500, "msg": f"识别失败: {e}", "data": {}}



if __name__ == "__main__":
    # html = _export_playlist_html('7512596145')
    # with open("playlist.html", "w", encoding="utf-8") as f:
    #     f.write(html)
    # print("✅ 精美歌单已生成到 playlist.html")
    
    # id0=_get_song_id("群青")
    # print("歌曲id",id0)
    
    # url=_get_music_url("届かない恋")
    # print("url:",url)
    
    # resp=_get_song_info("届かない恋 冬馬かずさ")
    # print(resp)
    
    # resp=_get_song_comment("海阔天空")
    # print(resp)
    
    # resp=_get_style_songs("二次元")
    # print(resp)
    
    resp=_get_artist_hot_songs("YOASObi")
    print(resp)
    
    # resp=_search_artist("YOASOBI")
    # print(resp)
    
    
    # res=_songs_recognize(r"F:\CloudMusic\split.mp3",
    #                  "233ac3bb36mshcc33feefaa6dba5p1df36cjsn5ccbf45c3865")
    # print(res)