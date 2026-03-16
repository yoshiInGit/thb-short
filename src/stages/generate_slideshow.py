import os
import json
from moviepy import ImageClip, CompositeVideoClip, vfx
from config import (
    SLIDESHOW_RESOLUTION, SLIDESHOW_OUTPUT_MP4, SLIDESHOW_FADE_DURATION,
    SLIDE_IMGS_DIR, FPS
)

def generate_slideshow(slide_imgs_data: dict):
    """
    slide_imgs.json のデータに基づいてスライドショー動画を生成する (MoviePy 2.0 準拠)
    """
    print("Running generate_slideshow (MoviePy 2.0)...")
    
    slides = slide_imgs_data.get("slide_imgs", [])
    if not slides:
        raise ValueError("No slide images data found.")

    clips = []
    w, h = SLIDESHOW_RESOLUTION

    for i, slide in enumerate(slides):
        img_filename = slide.get("img_path")
        time_start = float(slide.get("time_start")) / 1000.0
        time_end = float(slide.get("time_end")) / 1000.0
        duration = time_end - time_start

        if duration <= 0:
            continue

        img_path = os.path.join(SLIDE_IMGS_DIR, img_filename)
        if not os.path.exists(img_path):
            print(f"Warning: Image not found at {img_path}")
            continue

        # 画像を読み込み
        clip = ImageClip(img_path).with_duration(duration)

        # アスペクト比を維持してリサイズし、中央でクロップ（cover効果）
        img_w, img_h = clip.size
        aspect_ratio_img = img_w / img_h
        aspect_ratio_target = w / h

        if aspect_ratio_img > aspect_ratio_target:
            # 画像の方が横長い -> 高さをターゲットに合わせる
            new_h = h
            clip = clip.resized(height=new_h)
        else:
            # 画像の方が縦長い（または同じ） -> 幅をターゲットに合わせる
            new_w = w
            clip = clip.resized(width=new_w)

        # 中央でクロップ
        clip = clip.cropped(
            x_center=clip.w / 2,
            y_center=clip.h / 2,
            width=w,
            height=h
        )

        # フェード効果の適用 (MoviePy 2.0 では with_effects を推奨)
        clip = clip.with_effects([
            vfx.FadeIn(SLIDESHOW_FADE_DURATION),
            vfx.FadeOut(SLIDESHOW_FADE_DURATION)
        ])
        
        # 開始時間を設定
        clip = clip.with_start(time_start)
        clips.append(clip)

    # 全てのクリップを合成
    video = CompositeVideoClip(clips, size=SLIDESHOW_RESOLUTION)
    
    # 書き出し
    print(f"Writing slideshow to {SLIDESHOW_OUTPUT_MP4}...")
    video.write_videofile(SLIDESHOW_OUTPUT_MP4, fps=FPS, codec="libx264")
    print("Slideshow generation completed.")
