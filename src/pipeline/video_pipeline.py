import os
from stages.generate_voice_data import generate_voice_data
from stages.generate_video import generate_subtitle, generate_img_request
from stages.fetch_images import fetch_pixabay_images
from stages.generate_slideshow import generate_slideshow
from util.file_io import save_json
from config import (
    VOICE_DATA_JSON, OUTPUT_VOICE, IMG_REQUEST_JSON, 
    SLIDE_IMGS_JSON, OUTPUT_MP4, SLIDESHOW_OUTPUT_MP4, FPS
)

def gen_video_footage():
    """
    動画素材生成の一連のフローを実行するパイプライン
    1. generate_voice_data
    2. generate_subtitle
    3. generate_img_request
    4. fetch_images
    5. generate_slideshow
    """
    print("Starting video footage generation pipeline...")

    # 1. 音声データ生成
    print("\n--- Stage 1: Generate Voice Data ---")
    combined_audio, words_data = generate_voice_data()
    
    # 音声ファイルの保存
    combined_audio.export(OUTPUT_VOICE, format="wav")
    print(f"  -> Saved combined audio to {OUTPUT_VOICE}")
    
    # メタデータの保存
    voice_data = {"words": words_data}
    save_json(VOICE_DATA_JSON, voice_data)
    print(f"  -> Saved voice data to {VOICE_DATA_JSON}")

    # 2. 字幕生成
    print("\n--- Stage 2: Generate Subtitle ---")
    subtitle_clip = generate_subtitle(voice_data, audio_path=OUTPUT_VOICE)
    subtitle_clip.write_videofile(OUTPUT_MP4, fps=FPS, codec="libx264", audio_codec="aac")
    print(f"  -> Saved subtitle video to {OUTPUT_MP4}")

    # 3. 画像リクエスト生成
    print("\n--- Stage 3: Generate Image Request ---")
    img_req_res = generate_img_request(voice_data)
    save_json(IMG_REQUEST_JSON, img_req_res.model_dump())
    print(f"  -> Saved image request to {IMG_REQUEST_JSON}")

    # 4. 画像取得 (fetch_images)
    print("\n--- Stage 4: Fetch Images ---")
    # generate_img_request の結果をそのまま渡す（必要なら load_json し直すがここではメモリ上のデータを使用）
    slide_imgs_data = fetch_pixabay_images(img_req_res.model_dump())
    save_json(SLIDE_IMGS_JSON, slide_imgs_data)
    print(f"  -> Saved slide images info to {SLIDE_IMGS_JSON}")

    # 5. スライドショー生成
    print("\n--- Stage 5: Generate Slideshow ---")
    slides_clip = generate_slideshow(slide_imgs_data)
    if slides_clip:
        print(f"Writing slideshow to {SLIDESHOW_OUTPUT_MP4}...")
        slides_clip.write_videofile(SLIDESHOW_OUTPUT_MP4, fps=FPS, codec="libx264")
        print("Slideshow generation completed.")

    print("\nVideo footage generation pipeline finished successfully!")
