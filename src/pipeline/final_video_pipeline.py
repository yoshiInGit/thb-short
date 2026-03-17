import os
from stages.generate_voice_data import generate_voice_data
from stages.generate_video import generate_img_request
from stages.fetch_images import fetch_pixabay_images
from stages.generate_final_video import generate_final_video
from util.file_io import save_json
from config import (
    VOICE_DATA_JSON, OUTPUT_VOICE, IMG_REQUEST_JSON, 
    SLIDE_IMGS_JSON, FINAL_VIDEO_OUTPUT_MP4, FPS
)

def gen_final_video_pipeline():
    """
    最終的な動画（スライドショー + 音声 + 中央字幕）を生成する一連のフローを実行するパイプライン
    1. generate_voice_data
    2. generate_img_request
    3. fetch_images
    4. generate_final_video
    """
    print("Starting final video generation pipeline...")

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

    # 2. 画像リクエスト生成
    print("\n--- Stage 2: Generate Image Request ---")
    img_req_res = generate_img_request(voice_data)
    img_req_data = img_req_res.model_dump()
    save_json(IMG_REQUEST_JSON, img_req_data)
    print(f"  -> Saved image request to {IMG_REQUEST_JSON}")

    # 3. 画像取得 (fetch_images)
    print("\n--- Stage 3: Fetch Images ---")
    slide_imgs_data = fetch_pixabay_images(img_req_data)
    save_json(SLIDE_IMGS_JSON, slide_imgs_data)
    print(f"  -> Saved slide images info to {SLIDE_IMGS_JSON}")

    # 4. 最終動画合成
    print("\n--- Stage 4: Generate Final Video ---")
    
    # 4.1 スライドショークリップの生成
    from stages.generate_slideshow import generate_slideshow
    slides_clip = generate_slideshow(slide_imgs_data)
    if not slides_clip:
        print("Error: Failed to generate slideshow clip.")
        return

    # 4.2 音声の読み込み
    from moviepy import AudioFileClip
    audio = AudioFileClip(OUTPUT_VOICE)

    # 4.3 最終合成 (外部からクリップを渡す形式)
    final_clip = generate_final_video(slides_clip, audio, voice_data)
    
    if final_clip:
        print(f"Writing final video to {FINAL_VIDEO_OUTPUT_MP4}...")
        # 音声を含めて書き出し
        final_clip.write_videofile(FINAL_VIDEO_OUTPUT_MP4, fps=FPS, codec="libx264", audio_codec="aac")
        print("Final video generation completed.")
    else:
        print("Error: Final video generation failed.")

    print("\nFinal video generation pipeline finished successfully!")
