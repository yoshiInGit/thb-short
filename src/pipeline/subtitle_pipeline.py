from stages.generate_voice_data import generate_voice_data
from stages.generate_video import generate_subtitle
from util.file_io import save_json
from config import OUTPUT_VOICE, VOICE_DATA_JSON, OUTPUT_MP4, FPS

def gen_subtitle_pipeline():
    """音声データとメタデータの生成、および字幕動画の生成フローを実行する"""
    combined_audio, words_data = generate_voice_data()

    # 音声の保存
    combined_audio.export(OUTPUT_VOICE, format="wav")
    print(f"  -> Saved combined voice to {OUTPUT_VOICE}")

    # メタデータの保存
    voice_data = {"words": words_data}
    save_json(VOICE_DATA_JSON, voice_data)

    # 字幕動画の生成
    video_clip = generate_subtitle(voice_data)
    print(f"Exporting video to {OUTPUT_MP4}...")
    video_clip.write_videofile(OUTPUT_MP4, fps=FPS, codec="libx264", audio=False)
    print("Export complete!")
