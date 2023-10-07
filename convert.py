#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def merge_batch_subtitles(input_folder):
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".srt"):
                srt_path = os.path.join(root, file)
                ass_path = os.path.join(root, file.replace(".srt", ".danmu_utf8_cleaned.ass"))
                
                if os.path.exists(ass_path):
                    srt_to_ass(srt_path)
                    merge_ass_files(srt_path.replace(".srt", ".ass"), ass_path)

def round_time(time_str):
    hours, minutes, seconds = map(float, time_str.split(":"))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    rounded_seconds = round(total_seconds, 2)
    rounded_minutes, rounded_seconds = divmod(rounded_seconds, 60)
    rounded_hours, rounded_minutes = divmod(rounded_minutes, 60)
    return f"{int(rounded_hours):02}:{int(rounded_minutes):02}:{rounded_seconds:.2f}"

def srt_to_ass(input_file):
    output_file = os.path.splitext(input_file)[0] + ".ass"
    
    with open(input_file, 'r', encoding='utf-8') as srt_file:
        lines = srt_file.readlines()

    ass_lines = ["[Script Info]\n",
                 "Title: Converted ASS Subtitle\n",
                 "ScriptType: v4.00+\n",
                 "WrapStyle: 0\n",
                 "PlayResX: 1920\n",
                 "PlayResY: 1080\n",
                 "Timer: 10.0000\n",
                 "WrapStyle: 2\n",
                 "ScaledBorderAndShadow: no\n\n",
                 
                 "[V4+ Styles]\n",
				 "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n",
				 "Style: Default,Arial,60,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,2,2,0,0,30,1\n",
				 "Style: Alternate,Arial,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0.00,0.00,1,2.00,0.00,2,30,30,84,0\n",
				 "Style: Danmaku,Arial,38,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0.00,0.00,1,1.00,0.00,2,30,30,30,0\n\n",
				 
                 "[Events]\n",
                 "Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\n"]
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.isdigit():  # Assume it's a subtitle index
            i += 1  # Move to the next line (time)
            start, end = lines[i].strip().replace(',', '.').split(" --> ")[:2]  # Replace , with . and take first two parts
            start = round_time(start)
            end = round_time(end)
            i += 1  # Move to the next line (text)
            
            # Combine all text lines until an empty line is encountered
            text_lines = []
            while i < len(lines) and lines[i].strip():
                text_lines.append(lines[i].strip())
                i += 1
            
            text = "\\N".join(text_lines)  # Join text lines with \N (new line in ASS format)
            ass_lines.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")
        else:
            i += 1  # Move to the next line if the line is not a subtitle index

    with open(output_file, 'w', encoding='utf-8') as ass_file:
        ass_file.writelines(ass_lines)

def merge_ass_files(existing_ass_path, additional_ass_path):
    with open(existing_ass_path, 'r', encoding='utf-8') as existing_ass_file:
        existing_ass_lines = existing_ass_file.readlines()

    with open(additional_ass_path, 'r', encoding='utf-8') as additional_ass_file:
        additional_ass_lines = additional_ass_file.readlines()

    # Find the index where [Events] section starts in the existing ASS file
    events_index = existing_ass_lines.index("Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text\n") + 1

    # Add the Dialogue lines from the additional ASS file to the existing ASS file
    for line in additional_ass_lines:
        if line.startswith("Dialogue:"):
            existing_ass_lines.insert(events_index, line)

    # Write the updated content back to the existing ASS file
    with open(existing_ass_path, 'w', encoding='utf-8') as existing_ass_file:
        existing_ass_file.writelines(existing_ass_lines)

if __name__ == "__main__":
    input_folder = "/your_path/"  # Replace with the actual path to the folder containing the files 
    merge_batch_subtitles(input_folder)
