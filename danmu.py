#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from opencc import OpenCC

def convert_to_simplified_chinese(text):
    cc = OpenCC('t2s')  # t2s 表示繁体转简体
    simplified_text = cc.convert(text)
    return simplified_text

def is_valid_unicode(char):
    # 保留中文范围、ASCII码范围以及常见的标点符号
    return 0x4e00 <= ord(char) <= 0x9fff or 0x20 <= ord(char) <= 0x7E or char in ('。', '，', '！', '？', '：', '；', '“', '”', '‘', '’', '【', '】', '（', '）', '《', '》', '……', '—', '\n')

def remove_non_utf8_characters(text):
    return ''.join(char for char in text if is_valid_unicode(char))

def convert_ass_to_cleaned_utf8(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        ass_content = f.read()
    
    simplified_ass_content = ass_content
    utf8_cleaned_ass_content = remove_non_utf8_characters(simplified_ass_content)
    
    unicode_file_path = os.path.splitext(file_path)[0] + "_utf8_cleaned.ass"
    with codecs.open(unicode_file_path, 'w', encoding='utf-8') as f:
        f.write(utf8_cleaned_ass_content)
    
    print(f"Converted and saved: {unicode_file_path}")
    
    # 删除原始文件
    os.remove(file_path)
    print(f"Original file deleted: {file_path}")

def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('danmu.ass'):
                file_path = os.path.join(root, file)
                convert_ass_to_cleaned_utf8(file_path)

if __name__ == "__main__":
    folder_path = "/your_path/"
    process_folder(folder_path)
    print("Conversion to cleaned UTF-8 ASS complete.")


