import os
import textwrap
import json
import argparse
from moviepy import TextClip, ColorClip, CompositeVideoClip
from moviepy.video.fx import FadeIn, FadeOut
from google.genai import types
from models import ImgRequestResponse
from utils import load_prompt, save_log, generate_content_with_gemini, save_json, load_json
from config import VOICE_DATA_JSON, IMG_REQUEST_JSON, DEFAULT_MODEL, DEFAULT_TEMPERATURE, RESOLUTION, BG_COLOR, FPS, OUTPUT_DIR, OUTPUT_MP4, FONT_SIZE, FONT_COLOR, STROKE_COLOR, STROKE_WIDTH, FONT_NAME, WRAP_WIDTH, TEXT_POS

def generate_img_request(voice_data: dict) -> dict:
    """音声データをもとに、Geminiで画像リクエストを生成する"""
    print("Running generate_img_request...")
    
    # プロンプトの準備
    # voice_dataを文字列化して渡す
    voice_data_str = json.dumps(voice_data, ensure_ascii=False, indent=2)
    prompt = load_prompt("generate_img_request.txt", voice_data=voice_data_str)
    
    response = generate_content_with_gemini(
        model=DEFAULT_MODEL,
        prompt=prompt,
        response_schema=ImgRequestResponse,
        temperature=DEFAULT_TEMPERATURE
    )
    
    data = json.loads(response.text)
    save_log("generate_img_request", model, prompt, response.text)
    
    # 中間データの保存
    save_json(IMG_REQUEST_JSON, data)
    
    return data

def generate_subtitle(voice_data: dict):
    print("Running generate_subtitle...")

    words_data = voice_data.get("words", [])
    if not words_data:
        print("No words data found in JSON.")
        return

    # 最後の単語の終了時間をもとに総時間を計算(ミリ秒から秒へ)
    total_duration = max([float(w["time_end"]) / 1000.0 for w in words_data]) if words_data else 0

    # 背景(グリーンバック)のクリップを作成
    bg_clip = ColorClip(size=RESOLUTION, color=BG_COLOR, duration=total_duration)

    clips = [bg_clip]

    for item in words_data:
        word = item.get("word", "")
        # textwrap を使用して単語の途中で改行されないように処理
        wrapped_text = textwrap.fill(word, width=WRAP_WIDTH, break_long_words=False)
        
        # ミリ秒を秒に変換
        start_time = float(item["time_start"]) / 1000.0
        end_time = float(item["time_end"]) / 1000.0
        duration = end_time - start_time
        
        # 単語が空、または時間が異常な場合はスキップ
        if not word or duration <= 0:
            continue

        txt_clip = TextClip(
            text=wrapped_text, 
            font_size=FONT_SIZE, 
            color=FONT_COLOR, 
            font=FONT_NAME,
            stroke_color=STROKE_COLOR, 
            stroke_width=STROKE_WIDTH,
            method='caption',
            size=(int(RESOLUTION[0] * 0.9), None), # 横幅最大90%に拡大
            text_align='center'
        )
        
        
        txt_clip = txt_clip.with_position(TEXT_POS) \
                           .with_start(start_time) \
                           .with_duration(duration)
 
                               
        clips.append(txt_clip)

    # クリップを重ねて最終的な動画を作成
    final_video = CompositeVideoClip(clips)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Exporting video to {OUTPUT_MP4}...")
    final_video.write_videofile(OUTPUT_MP4, fps=FPS, codec="libx264", audio=False)
    print("Export complete!")

def main():
    parser = argparse.ArgumentParser(description="動画生成支援ツール")
    parser.add_argument("command", choices=["gen-img-req", "gen-sub"], help="実行するコマンド")
    args = parser.parse_args()

    if args.command == "gen-img-req":
        voice_data = load_json(VOICE_DATA_JSON)
        generate_img_request(voice_data)
    elif args.command == "gen-sub":
        voice_data = load_json(VOICE_DATA_JSON)
        generate_subtitle(voice_data)

if __name__ == "__main__":
    main()
