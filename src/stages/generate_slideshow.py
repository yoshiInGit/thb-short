import os
import numpy as np
from moviepy import ImageClip, CompositeVideoClip, vfx
from model.video import SlideImgsResponse, SlideItem
from config import (
    SLIDESHOW_RESOLUTION, SLIDESHOW_OUTPUT_MP4, SLIDESHOW_FADE_DURATION,
    SLIDE_IMGS_DIR, FPS
)

def _apply_cover_layout(clip: ImageClip, target_size: tuple[int, int]) -> ImageClip:
    """
    アスペクト比を維持しつつ、指定されたサイズを完全に覆うようにリサイズし、中央でクロップする
    """
    target_w, target_h = target_size
    img_w, img_h = clip.size
    
    aspect_ratio_img = img_w / img_h
    aspect_ratio_target = target_w / target_h

    if aspect_ratio_img > aspect_ratio_target:
        # 画像の方が横長い -> 高さをターゲットに合わせる
        clip = clip.resized(height=target_h)
    else:
        # 画像の方が縦長い（または同じ） -> 幅をターゲットに合わせる
        clip = clip.resized(width=target_w)

    # 中央でクロップ
    return clip.cropped(
        x_center=clip.w / 2,
        y_center=clip.h / 2,
        width=target_w,
        height=target_h
    )

def _create_slide_clip(slide: SlideItem) -> ImageClip | None:
    """
    個別のスライド項目から MoviePy のクリップを生成する
    """
    time_start_s = float(slide.time_start) / 1000.0
    time_end_s = float(slide.time_end) / 1000.0
    duration = time_end_s - time_start_s

    if duration <= 0:
        return None

    img_path = os.path.join(SLIDE_IMGS_DIR, slide.img_path)
    if not os.path.exists(img_path):
        print(f"Warning: Image not found at {img_path}")
        return None

    # クリップ生成
    clip = ImageClip(img_path).with_duration(duration)
    
    # グレースケール画像 (H, W) の場合、(H, W, 3) に変換
    # MoviePy 2.x のエフェクト(FadeIn等)でのブロードキャストエラー回避のため
    if len(clip.img.shape) == 2:
        clip.img = np.stack([clip.img] * 3, axis=-1)
    
    # レイアウト適用 (Cover Crop)
    clip = _apply_cover_layout(clip, SLIDESHOW_RESOLUTION)

    # エフェクト適用 (MoviePy 2.0)
    clip = clip.with_effects([
        vfx.FadeIn(SLIDESHOW_FADE_DURATION),
        vfx.FadeOut(SLIDESHOW_FADE_DURATION)
    ])
    
    # 開始時間設定
    return clip.with_start(time_start_s)

def generate_slideshow(slide_imgs_data: dict) -> CompositeVideoClip | None:
    """
    slide_imgs.json のデータに基づいてスライドショー動画を生成する
    """
    print("Running generate_slideshow (Refactored)...")
    
    # Pydantic モデルによるパースとバリデーション
    response = SlideImgsResponse(**slide_imgs_data)
    
    clips = []
    for slide in response.slide_imgs:
        clip = _create_slide_clip(slide)
        if clip:
            clips.append(clip)

    if not clips:
        print("Error: No valid clips generated.")
        return None

    # 全てのクリップを合成
    video = CompositeVideoClip(clips, size=SLIDESHOW_RESOLUTION)
    
    return video
