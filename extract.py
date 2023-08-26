#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os

def extract_all_subtitles(video_path, ffmpeg_path):
    # 获取视频文件的基本文件名（不包括扩展名）
    base_filename = os.path.splitext(os.path.basename(video_path))[0]

    # 构建ffmpeg命令，提取所有字幕流并保存为SRT文件
    command = [
        ffmpeg_path, '-i', video_path,
        '-map', '0:s:1',       # 选择所有内嵌字幕流
        '-c:s', 'srt',       # 将字幕转换为SRT格式
        f"{os.path.dirname(video_path)}/{base_filename}.srt"  # 字幕文件名
    ]

    # 运行ffmpeg命令
    try:
        subprocess.run(command, check=True)
        print("所有字幕提取成功并保存在目录", os.path.dirname(video_path))
    except subprocess.CalledProcessError as e:
        print("字幕提取失败:", e)

if __name__ == "__main__":
    root_folder = "/your_path/"
    ffmpeg_path = "/your_path/ffmpeg"

    if os.path.exists(root_folder):
        video_files = [f for f in os.listdir(root_folder) if f.lower().endswith(('.mp4', '.mkv', '.avi'))]# 视频格式匹配
        for video_file in video_files:
            video_path = os.path.join(root_folder, video_file)
            extract_all_subtitles(video_path, ffmpeg_path)
    else:
        print("文件夹不存在")