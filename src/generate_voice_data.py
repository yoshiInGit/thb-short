import os
import glob
import json
from pydub import AudioSegment

# ===== Constants & Paths =====
OUTPUT_DIR = "output"
INTERMEDIATE_DIR = os.path.join(OUTPUT_DIR, "intermediate")
VOICE_DIR = "input/voice"
OUTPUT_VOICE = os.path.join(OUTPUT_DIR, "voice.wav")
OUTPUT_JSON = os.path.join(INTERMEDIATE_DIR, "voice_data.json")
SILENCE_DURATION_MS = 250

def _get_sorted_wav_files(directory: str) -> list:
    """ディレクトリから連番順にソートされたWAVファイルのリストを返す"""
    wav_files = glob.glob(os.path.join(directory, "*.wav"))
    
    def get_index(filepath):
        basename = os.path.basename(filepath)
        num_str = basename.split("_")[0]
        try:
            return int(num_str)
        except ValueError:
            return 999999
            
    wav_files.sort(key=get_index)
    return wav_files

def _get_accompanying_text(wav_path: str) -> str:
    """音声ファイルに対応するテキストファイルの内容を読み取る"""
    txt_path = wav_path.rsplit(".", 1)[0] + ".txt"
    if not os.path.exists(txt_path):
        print(f"Warning: Text file for {wav_path} not found.")
        return ""
    
    with open(txt_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def _has_punctuation_at_end(text: str) -> bool:
    """テキストの末尾が句読点かどうかを判定する"""
    if not text:
        return False
    punctuations = ("、", "。", "！", "？", "!", "?", "…")
    return text[-1] in punctuations

def generate_voice_data():
    """音声ファイルの結合とメタデータ(JSON)の生成を行う"""
    print("Running generate_voice_data...")
    
    if not os.path.exists(VOICE_DIR):
        print(f"Error: Voice directory {VOICE_DIR} not found.")
        return

    wav_files = _get_sorted_wav_files(VOICE_DIR)
    combined_audio = AudioSegment.empty()
    words_data = []
    current_time_ms = 0
    previous_text = ""


    for wav_path in wav_files:
        # 1. 音声に対応するテキストの内容を取得
        word_text = _get_accompanying_text(wav_path)
                
        # 2. 音声ファイルを AudioSegment オブジェクトとして読み込む
        try:
            audio_segment = AudioSegment.from_wav(wav_path)
        except Exception as e:
            print(f"Error reading {wav_path}: {e}")
            continue
            
        # 3. 句読点判定による無音(ポーズ)の挿入
        # 直前の言葉が句読点等で終わっている場合、SILENCE_DURATION_MS 分の無音を追加
        if _has_punctuation_at_end(previous_text):
            combined_audio += AudioSegment.silent(duration=SILENCE_DURATION_MS)
            current_time_ms += SILENCE_DURATION_MS
            
        duration_ms = len(audio_segment)
        
        # 4. JSONに出力するためのタイムスタンプ(開始・終了時間、単位:ms)を記録
        words_data.append({
            "word": word_text,
            "time_start": current_time_ms,
            "time_end": current_time_ms + duration_ms
        })
        
        # 5. 音声の結合と時間の更新、直前テキストの保持
        combined_audio += audio_segment
        current_time_ms += duration_ms
        previous_text = word_text

    # 成果物の保存
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    combined_audio.export(OUTPUT_VOICE, format="wav")
    print(f"  -> Saved combined voice to {OUTPUT_VOICE}")
    
    os.makedirs(INTERMEDIATE_DIR, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump({"words": words_data}, f, ensure_ascii=False, indent=2)
    print(f"  -> Saved voice data JSON to {OUTPUT_JSON}")

    return OUTPUT_JSON

if __name__ == "__main__":
    generate_voice_data()
