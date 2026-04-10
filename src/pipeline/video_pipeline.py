from moviepy import AudioFileClip
from stages.generate_voice_data import generate_voice_data
from stages.generate_video import generate_subtitle
from util.file_io import save_json
from config import (
    VOICE_DATA_JSON, OUTPUT_VOICE, OUTPUT_MP4, FPS
)

def gen_video_footage():
    """
    動画素材生成の一連のフローを実行するパイプライン
    1. generate_voice_data
    2. generate_subtitle
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
    audio_clip = AudioFileClip(OUTPUT_VOICE)
    subtitle_clip = generate_subtitle(voice_data, audio_clip=audio_clip)
    subtitle_clip.write_videofile(OUTPUT_MP4, fps=FPS, codec="libx264", audio_codec="aac")
    print(f"  -> Saved subtitle video to {OUTPUT_MP4}")

    print("\nVideo footage generation pipeline finished successfully!")
