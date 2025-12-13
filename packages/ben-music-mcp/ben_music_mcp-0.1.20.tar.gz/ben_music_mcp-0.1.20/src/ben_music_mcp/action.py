import platform

if platform.system() == "Windows":
    import uiautomation as auto
    import time
    import subprocess
    import psutil
    import pyautogui

    exe_path0 = r'C:\CloudMusic\cloudmusic.exe'
    def _open_cloud_music(exe_path: str = None):
        """
        打开网易云音乐客户端。
        exe_path: 可选，指定客户端路径。如果输入则更新默认路径。
        """
        global exe_path0
        try:
            if exe_path:
                exe_path0 = exe_path
            path_to_use = exe_path0
            found = False
            for w in auto.GetRootControl().GetChildren():
                pid = w.ProcessId
                try:
                    proc = psutil.Process(pid)
                    if proc.name().lower() == 'cloudmusic.exe':
                        w.SetActive()
                        found = True
                        break
                except Exception:
                    continue
            if not found:
                subprocess.Popen(path_to_use)
                time.sleep(2)  # 等待程序启动
            return {"code": 200, "msg": "网易云音乐已启动"}
        except Exception as e:
            return {"code": 500, "msg": f"启动失败: {e}"}

    def _search_and_play(keyword:str, timeout:float=0.2):
        try:
            _open_cloud_music()
            pyautogui.click(447, 43)  # 点击输入框
            time.sleep(timeout)
            auto.SendKeys(keyword)  # 输入搜索内容，这个还是uiautomation好用
            time.sleep(timeout)
            pyautogui.click(380, 42)  # 点击搜索框
            time.sleep(timeout)
            pyautogui.click(392, 190)  # 点击“单曲”
            time.sleep(1)
            pyautogui.doubleClick(402, 339)  # 双击“第一首”播放
            return {"code": 200, "msg": f"已成功播放歌曲: {keyword}"}
        except Exception as e:
            return {"code": 500, "msg": f"播放歌曲失败: {e}"}

    def _play_and_pause():
        try:
            _open_cloud_music()
            pyautogui.click(961, 1028)  # 点击播放按钮
            return {"code": 200, "msg": "成功【播放】/【暂停】"}
        except Exception as e:
            return {"code": 500, "msg": f"操作失败: {e}"}

    def _next_song():
        try:
            _open_cloud_music()
            pyautogui.click(1025, 1032)  # 点击下一首按钮
            return {"code": 200, "msg": "切换下一首成功"}
        except Exception as e:
            return {"code": 500, "msg": f"操作失败: {e}"}

    def _pre_song():
        try:
            _open_cloud_music()
            pyautogui.click(894, 1028)  # 点击上一首按钮
            return {"code": 200, "msg": "切换上一首成功"}
        except Exception as e:
            return {"code": 500, "msg": f"操作失败: {e}"}

else:
    exe_path0 = None
    def _open_cloud_music(exe_path: str = None):
        return {"code": 501, "msg": "本功能仅支持 Windows 环境，请本地 Local 使用 uvx ben-music-mcp@latest"}
    
    def _search_and_play(keyword: str, timeout: float = 0.2):
        return {"code": 501, "msg": "本功能仅支持 Windows 环境，请本地 Local 使用 uvx ben-music-mcp@latest"}

    def _play_and_pause():
        return {"code": 501, "msg": "本功能仅支持 Windows 环境，请本地 Local 使用 uvx ben-music-mcp@latest"}

    def _next_song():
        return {"code": 501, "msg": "本功能仅支持 Windows 环境，请本地 Local 使用 uvx ben-music-mcp@latest"}

    def _pre_song():
        return {"code": 501, "msg": "本功能仅支持 Windows 环境，请本地 Local 使用 uvx ben-music-mcp@latest"}


if __name__ == "__main__":
    # _open_cloud_music()
    
    # _search_and_play("打上花火")
    
    # _play_and_pause()
    
    # _next_song()
    
    _pre_song()