import os
import json
from moviepy import TextClip, CompositeVideoClip, AudioFileClip, VideoClip
from config import (
    SLIDESHOW_RESOLUTION, FONT_SIZE, FONT_COLOR, 
    STROKE_COLOR, STROKE_WIDTH, FONT_NAME
)

def generate_final_video(slides_clip: VideoClip, audio: AudioFileClip, voice_data: dict) -> CompositeVideoClip | None:
    """
    スライドショー、音声、及び中央配置の字幕を統合した最終的な動画を生成する
    """
    print("Running generate_final_video...")

    # 1. 音声の適用
    slides_clip = slides_clip.with_audio(audio)

    # 2. 字幕クリップの生成 (指示に従い、既存関数を流用せず新規実装)
    # ターゲット解像度はスライドショーに準ずる
    target_size = SLIDESHOW_RESOLUTION
    
    words_data = voice_data.get("words", [])
    subtitle_clips = []
    
    for item in words_data:
        start_time_s = float(item["time_start"]) / 1000.0
        end_time_s   = float(item["time_end"]) / 1000.0
        duration_s   = end_time_s - start_time_s

        word = item.get("word", "")
        if not word or duration_s <= 0:
            continue

        # 中央に表示するためのテキストクリップ
        # method='caption' でサイズ指定すると自動で中央揃えや折り返しが行われる
        txt_clip = TextClip(
            text=word, 
            font_size=FONT_SIZE, 
            color=FONT_COLOR, 
            font=FONT_NAME,
            stroke_color=STROKE_COLOR, 
            stroke_width=STROKE_WIDTH,
            method='caption',
            size=(int(target_size[0] * 0.8), None), # 横幅の80%程度に制限
            text_align='center'
        )
        
        # 位置を中央(center, center)に設定
        txt_clip = txt_clip.with_position(('center', 'center')) \
                           .with_start(start_time_s) \
                           .with_duration(duration_s)
        
        subtitle_clips.append(txt_clip)

    # 4. スライドショーと字幕を合成
    # 字幕をスライドショーの上に重ねる
    final_video = CompositeVideoClip([slides_clip] + subtitle_clips, size=target_size)
    
    # 動画全体の長さは音声またはスライドショーの長い方に合わせる（通常は一致するはず）
    final_video = final_video.with_duration(audio.duration)

    return final_video
