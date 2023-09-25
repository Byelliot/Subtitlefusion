# 简介
从视频中提取 srt 字幕并将 srt 合并到 ass，适用于 Jellyfin/Emby 等媒体服务器无法同时挂载两个字幕的解决方法，多用于字幕和弹幕融合
  
# 环境准备
- Python 3.8 
- ffmpeg 
- Codecs （pip install codecs ）

# 使用
## 1.提取视频srt字幕 
使用extract.py 修改 path（具体文件）
```python
root_folder = "/your_path/" #目标视频 
ffmpeg_path = "/your_path/ffmpeg" #ffmpeg路径
```
## 2.合并字幕
使用convert.py 修改 path（目录）
```python
input_folder = "/your_path/"  #替换需要合并字幕的目录
```
匹配ass
```python
ass_path = os.path.join(root, file.replace(".srt", ".danmu_utf8_cleaned.ass")) #匹配ass 
```
## 3.Kodi ass乱码（将ass文件保存为UTF-8，可在nas中设置定时任务）
使用danmu.py 修改 path（目录）
```python
folder_path = "/your_path/" #替换需要重新编码的目录
```
匹配ass
```python
if file.lower().endswith('danmu.ass'): #匹配ass  
```
# 其他
配合弹幕下载插件食用更香（jellyfin） [https://github.com/cxfksword/jellyfin-plugin-danmu ](https://github.com/cxfksword/jellyfin-plugin-danmu)https://github.com/cxfksword/jellyfin-plugin-danmu
