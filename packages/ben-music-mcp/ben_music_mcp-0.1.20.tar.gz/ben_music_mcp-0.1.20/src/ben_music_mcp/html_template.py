"""
HTML 模板生成模块
用于生成歌单展示页面的 HTML
"""

def generate_playlist_html(playlist: dict, base_url: str) -> str:
    """
    根据歌单详情生成精美的交互式 HTML 展示页面
    :param playlist: _get_playlist 返回的 dict
    :param base_url: API 基础 URL
    :return: HTML 字符串
    """
    if not playlist or "id" not in playlist:
        return "<p>未找到歌单信息</p>"

    # 格式化播放量和订阅量
    def format_number(num):
        if num >= 100000000:
            return f"{num/100000000:.1f}亿"
        elif num >= 10000:
            return f"{num/10000:.1f}万"
        return str(num)

    # 格式化时间戳
    def format_time(timestamp):
        if not timestamp:
            return ""
        from datetime import datetime
        return datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d')

    play_count = format_number(playlist.get('playCount', 0))
    subscribe_count = format_number(playlist.get('subscribedCount', 0))
    create_time = format_time(playlist.get('createTime', 0))
    
    # CSS 样式
    css_styles = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
            min-height: 100vh;
            padding: 20px;
            animation: gradientShift 15s ease infinite;
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: fadeInUp 0.6s ease;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            color: white;
            display: flex;
            gap: 30px;
            align-items: flex-start;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: headerGlow 8s ease-in-out infinite;
        }
        
        @keyframes headerGlow {
            0%, 100% { transform: translate(0, 0); }
            50% { transform: translate(-20%, -20%); }
        }
        
        .cover-container {
            flex-shrink: 0;
            position: relative;
            z-index: 1;
        }
        
        .cover {
            width: 220px;
            height: 220px;
            border-radius: 15px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
            object-fit: cover;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border: 3px solid rgba(255, 255, 255, 0.2);
        }
        
        .cover:hover {
            transform: scale(1.08) rotate(2deg);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        }
        
        .info {
            flex: 1;
            position: relative;
            z-index: 1;
        }
        
        .playlist-title {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            animation: titleSlideIn 0.8s ease;
        }
        
        @keyframes titleSlideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }
        
        .tag {
            background: rgba(255, 255, 255, 0.25);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 14px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
        }
        
        .tag:hover {
            background: rgba(255, 255, 255, 0.35);
            transform: translateY(-2px);
        }
        
        .stats {
            display: flex;
            gap: 25px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .stat-item {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        
        .stat-label {
            font-size: 13px;
            opacity: 0.9;
        }
        
        .stat-value {
            font-size: 20px;
            font-weight: bold;
        }
        
        .description {
            margin-top: 15px;
            line-height: 1.6;
            opacity: 0.95;
            max-width: 600px;
        }
        
        .content {
            padding: 30px 40px;
        }
        
        .section-title {
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        
        .track-list {
            list-style: none;
        }
        
        .track-item {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            border-radius: 10px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            gap: 15px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .track-item::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            transform: scaleY(0);
            transition: transform 0.3s ease;
        }
        
        .track-item:hover::before {
            transform: scaleY(1);
        }
        
        .track-item:hover {
            background: linear-gradient(90deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
            transform: translateX(8px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }
        
        .track-item:active {
            transform: translateX(8px) scale(0.98);
        }
        
        .track-number {
            font-size: 16px;
            font-weight: bold;
            color: #999;
            min-width: 35px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .track-item:hover .track-number {
            color: #667eea;
            transform: scale(1.1);
        }
        
        .track-info {
            flex: 1;
            min-width: 0;
        }
        
        .track-name {
            font-size: 16px;
            font-weight: 500;
            color: #333;
            margin-bottom: 5px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .track-artists {
            font-size: 14px;
            color: #666;
        }
        
        .track-album {
            font-size: 14px;
            color: #999;
            min-width: 200px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .track-alias {
            font-size: 13px;
            color: #999;
            font-style: italic;
        }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(5px);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .modal-content {
            position: relative;
            background: white;
            margin: 5% auto;
            padding: 0;
            width: 90%;
            max-width: 800px;
            max-height: 80vh;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            overflow: hidden;
            animation: modalSlideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        @keyframes modalSlideIn {
            from {
                transform: translateY(-50px) scale(0.9);
                opacity: 0;
            }
            to {
                transform: translateY(0) scale(1);
                opacity: 1;
            }
        }
        
        .modal-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 30px;
        }
        
        .modal-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 8px;
        }
        
        .modal-artist {
            font-size: 16px;
            opacity: 0.9;
        }
        
        .close {
            position: absolute;
            right: 20px;
            top: 20px;
            color: white;
            font-size: 32px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
        }
        
        .close:hover {
            transform: rotate(90deg) scale(1.1);
            background: rgba(255, 255, 255, 0.2);
        }
        
        .modal-body {
            padding: 30px;
            max-height: 60vh;
            overflow-y: auto;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #999;
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; }
        }
        
        .audio-player {
            background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            animation: slideInLeft 0.4s ease;
        }
        
        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .audio-player audio {
            width: 100%;
            border-radius: 8px;
        }
        
        .lyric-container {
            background: linear-gradient(135deg, #fafbfc 0%, #f0f2f5 100%);
            padding: 20px;
            border-radius: 12px;
            line-height: 2;
            white-space: pre-wrap;
            max-height: 400px;
            overflow-y: auto;
            box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.05);
            animation: slideInRight 0.4s ease;
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .lyric-container::-webkit-scrollbar {
            width: 8px;
        }
        
        .lyric-container::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.05);
            border-radius: 4px;
        }
        
        .lyric-container::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
        }
        
        .lyric-container::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #5568d3 0%, #653b8a 100%);
        }
        
        .error-message {
            color: #e74c3c;
            padding: 20px;
            text-align: center;
            background: rgba(231, 76, 60, 0.1);
            border-radius: 8px;
            border-left: 4px solid #e74c3c;
            animation: shake 0.5s ease;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        
        @media (max-width: 768px) {
            .header {
                flex-direction: column;
                align-items: center;
                text-align: center;
            }
            
            .stats {
                justify-content: center;
            }
            
            .track-album {
                display: none;
            }
            
            .content {
                padding: 20px;
            }
            
            .modal-content {
                width: 95%;
                margin: 10% auto;
            }
        }
    """
    
    # JavaScript 代码
    javascript_code = f"""
        const BASE_URL = '{base_url}';
        
        // 平滑滚动到顶部
        function scrollToTop() {{
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}
        
        function showSongDetail(songId, songName, artistName) {{
            const modal = document.getElementById('songModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalArtist = document.getElementById('modalArtist');
            const modalBody = document.getElementById('modalBody');
            
            modal.style.display = 'block';
            modalTitle.textContent = songName;
            modalArtist.textContent = '🎤 ' + artistName;
            modalBody.innerHTML = '<div class="loading">🎵 正在加载歌曲信息...</div>';
            
            // 添加淡入动画
            requestAnimationFrame(() => {{
                modal.style.opacity = '1';
            }});
            
            Promise.all([
                fetch(`https://music-api.gdstudio.xyz/api.php?types=lyric&source=netease&id=${{songId}}`),
                fetch(`https://music-api.gdstudio.xyz/api.php?types=url&source=netease&id=${{songId}}&br=128`)
            ])
            .then(responses => Promise.all(responses.map(r => r.json())))
            .then(([lyricData, urlData]) => {{
                let html = '';
                console.log('API返回数据:', urlData);
                
                if (urlData && urlData.url) {{
                    const songUrl = urlData.url;
                    if (songUrl) {{
                        html += `
                            <div class="audio-player">
                                <h3 style="margin-bottom: 15px; color: #667eea;">🎧 在线播放</h3>
                                <audio controls autoplay>
                                    <source src="${{songUrl}}" type="audio/mpeg">
                                    您的浏览器不支持音频播放。
                                </audio>
                            </div>
                        `;
                    }} else {{
                        html += '<div class="error-message">⚠️ 该歌曲暂无播放链接</div>';
                    }}
                }} else {{
                    html += '<div class="error-message">⚠️ 获取播放链接失败，可能是API限制</div>';
                }}
                if (lyricData && lyricData.lyric) {{
                    const lyrics = lyricData.lyric;
                    const cleanLyrics = lyrics.replace(/\\[\\d{{2}}:\\d{{2}}\\.\\d{{2,3}}\\]/g, '').trim();
                    html += `
                        <div style="margin-top: 20px;">
                            <h3 style="margin-bottom: 15px; color: #667eea;">📝 歌词</h3>
                            <div class="lyric-container">${{cleanLyrics || '暂无歌词'}}</div>
                        </div>
                    `;
                }} else {{
                    html += '<div style="margin-top: 20px;"><h3 style="color: #667eea;">📝 歌词</h3><div class="lyric-container">暂无歌词</div></div>';
                }}
                
                modalBody.innerHTML = html;
            }})
            .catch(error => {{
                console.error('加载错误:', error);
                modalBody.innerHTML = '<div class="error-message">❌ 加载失败，请稍后重试</div>';
            }});
        }}
        
        function closeModal() {{
            const modal = document.getElementById('songModal');
            modal.style.opacity = '0';
            setTimeout(() => {{
                modal.style.display = 'none';
            }}, 300);
            
            const audios = document.querySelectorAll('audio');
            audios.forEach(audio => {{
                audio.pause();
                audio.currentTime = 0;
            }});
        }}
        
        window.onclick = function(event) {{
            const modal = document.getElementById('songModal');
            if (event.target === modal) {{
                closeModal();
            }}
        }}
        
        document.addEventListener('keydown', function(event) {{
            if (event.key === 'Escape') {{
                closeModal();
            }}
        }});
        
        // 页面加载完成后添加淡入效果
        window.addEventListener('load', function() {{
            document.body.style.opacity = '1';
        }});
    """
    
    # 构建完整 HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{playlist.get('name', '歌单')}</title>
    <style>{css_styles}</style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="cover-container">
                <img class="cover" src="{playlist.get('coverImgUrl', '')}" alt="封面" onerror="this.src='https://via.placeholder.com/220?text=No+Image'">
            </div>
            <div class="info">
                <h1 class="playlist-title">{playlist.get('name', '未命名歌单')}</h1>
                <div class="tags">
"""
    
    # 添加标签
    tags = playlist.get('tags', [])
    if tags:
        for tag in tags:
            html += f'                    <span class="tag">#{tag}</span>\n'
    else:
        html += '                    <span class="tag">#音乐</span>\n'
    
    html += f"""                </div>
                <div class="stats">
                    <div class="stat-item">
                        <span class="stat-label">📅 创建时间</span>
                        <span class="stat-value">{create_time}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">🎵 歌曲数</span>
                        <span class="stat-value">{playlist.get('trackCount', 0)}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">▶️ 播放量</span>
                        <span class="stat-value">{play_count}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">❤️ 订阅量</span>
                        <span class="stat-value">{subscribe_count}</span>
                    </div>
                </div>
"""
    
    # 添加简介
    description = playlist.get('description', '')
    if description:
        html += f'                <div class="description">{description}</div>\n'
    
    html += """            </div>
        </div>
        
        <div class="content">
            <h2 class="section-title">歌曲列表（点击查看详情）</h2>
            <ul class="track-list">
"""
    
    # 添加歌曲列表
    for idx, track in enumerate(playlist.get("tracks", []), 1):
        track_id = track.get('id', '')
        track_name = track.get('name', '未知歌曲')
        track_artists = ', '.join(track.get('ar', ['未知歌手']))
        track_album = track.get('al', '未知专辑')
        track_alias = ', '.join(track.get('alia', []))
        
        html += f"""                <li class="track-item" onclick="showSongDetail({track_id}, '{track_name}', '{track_artists}')">
                    <div class="track-number">{idx}</div>
                    <div class="track-info">
                        <div class="track-name">{track_name}</div>
                        <div class="track-artists">🎤 {track_artists}</div>
"""
        if track_alias:
            html += f'                        <div class="track-alias">({track_alias})</div>\n'
        
        html += f"""                    </div>
                    <div class="track-album">💿 {track_album}</div>
                </li>
"""
    
    html += """            </ul>
        </div>
    </div>
    
    <!-- 歌曲详情模态框 -->
    <div id="songModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span class="close" onclick="closeModal()">&times;</span>
                <h2 class="modal-title" id="modalTitle">歌曲名称</h2>
                <p class="modal-artist" id="modalArtist">歌手名称</p>
            </div>
            <div class="modal-body" id="modalBody">
                <div class="loading">🎵 正在加载...</div>
            </div>
        </div>
    </div>
    
    <script>""" + javascript_code + """</script>
</body>
</html>"""
    
    return html
