import os
import json
from moviepy import TextClip, ColorClip, CompositeVideoClip
from model.video import ImgRequestResponse
from util.prompt import load_prompt
from util.gemini import generate_structured_content
from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, RESOLUTION, BG_COLOR, FONT_SIZE, FONT_COLOR, STROKE_COLOR, STROKE_WIDTH, FONT_NAME, TEXT_POS, TEXT_MARGIN_RIGHT

def generate_img_request(voice_data: dict) -> ImgRequestResponse:
    """音声データをもとに、Geminiで画像リクエストを生成する"""
    print("Running generate_img_request...")
    
    # voice_dataを文字列化して渡す
    voice_data_str = json.dumps(voice_data, ensure_ascii=False, indent=2)
    prompt = load_prompt("generate_img_request.txt", voice_data=voice_data_str)
    
    return generate_structured_content(
        func_name="generate_img_request",
        model=DEFAULT_MODEL,
        prompt=prompt,
        response_schema=ImgRequestResponse,
        temperature=DEFAULT_TEMPERATURE
    )

def generate_subtitle(voice_data: dict) -> CompositeVideoClip:
    """音声データをもとに字幕動画（CompositeVideoClip）を生成する"""
    print("Running generate_subtitle...")

    words_data = voice_data.get("words", [])
    if not words_data:
        raise ValueError("No words data found in JSON.")

    # 最後の単語の終了時間をもとに総時間を計算(ミリ秒から秒へ)
    total_duration_s = max([float(w["time_end"]) / 1000.0 for w in words_data])

    # 背景(グリーンバック)のクリップを作成
    bg_clip = ColorClip(size=RESOLUTION, color=BG_COLOR, duration=total_duration_s)

    clips = [bg_clip]
    for item in words_data:
        start_time_s = float(item["time_start"]) / 1000.0
        end_time_s   = float(item["time_end"]) / 1000.0
        duration_s   = end_time_s - start_time_s

        word = item.get("word", "")
        if not word or duration_s <= 0:
            continue

        # X軸の位置に基づいて、画面をはみ出さないスマートな幅を計算
        text_x = TEXT_POS[0] if isinstance(TEXT_POS[0], int) else 0
        max_width = RESOLUTION[0] - text_x - TEXT_MARGIN_RIGHT

        # テキストクリップの作成
        txt_clip = TextClip(
            text=word, 
            font_size=FONT_SIZE, 
            color=FONT_COLOR, 
            font=FONT_NAME,
            stroke_color=STROKE_COLOR, 
            stroke_width=STROKE_WIDTH,
            method='caption',
            size=(max_width, None),
            text_align='left'
        )
        
        txt_clip = txt_clip.with_position(TEXT_POS) \
                           .with_start(start_time_s) \
                           .with_duration(duration_s)
        clips.append(txt_clip)

    return CompositeVideoClip(clips)
