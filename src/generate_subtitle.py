import os
import textwrap
from moviepy import TextClip, ColorClip, CompositeVideoClip
from moviepy.video.fx import FadeIn, FadeOut

# ===== Configurations =====
RESOLUTION = (1080, 1920)
BG_COLOR = (0, 255, 0) # Green back
FPS = 1
OUTPUT_DIR = "output"
OUTPUT_MP4 = os.path.join(OUTPUT_DIR, "subtitle.mp4")

# Text Configuration
FONT_SIZE = 72
FONT_COLOR = "white"
STROKE_COLOR = "black"
STROKE_WIDTH = 3
FONT_NAME = "assets/font/LINESeedJP-Bold.ttf" 
WRAP_WIDTH = 12  # 1行あたりの最大文字数
# 字幕の表示位置 ('center', 'top', 'bottom' や (x, y) のタプルで指定可能)
# 例: ('center', 1400) で中央やや下に配置
TEXT_POS = ('center', 580)
TRANSITION_DURATION = 0.2  # フェードイン・アウトの時間(秒)

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
 \
                               
        clips.append(txt_clip)

    # クリップを重ねて最終的な動画を作成
    final_video = CompositeVideoClip(clips)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Exporting video to {OUTPUT_MP4}...")
    final_video.write_videofile(OUTPUT_MP4, fps=FPS, codec="libx264", audio=False)
    print("Export complete!")

