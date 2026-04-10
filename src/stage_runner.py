import os
import argparse
from stages.generate_script import make_script, add_character_script, output_coeroink_txt
from stages.generate_video import generate_subtitle
from stages.generate_voice_data import generate_voice_data
from util.file_io import load_json, save_json
from util.prompt import read_prompt_template
from config import (
    VOICE_DATA_JSON, TRIVIA_INPUT_PATH, THEME_INPUT_PATH,
    OUTPUT_VOICE, OUTPUT_MP4, FPS,
    MAKE_SCRIPT_PROMPT_FILE, MAKE_SCRIPT_VERIFY_PROMPT_FILE,
    ADD_CHARACTER_SCRIPT_PROMPT_FILE, OUTPUT_COEROINK_TXT_PROMPT_FILE
)
from moviepy import AudioFileClip

def _parse_args():
    """コマンドライン引数の解析"""
    parser = argparse.ArgumentParser(description="THB Short 各工程（ステージ）単独実行ツール")
    parser.add_argument("stage", choices=["make-script", "add-char", "coeroink", "gen-voice", "gen-subtitle"], help="実行するステージ")
    
    return parser.parse_args(), parser

def main():
    args, parser = _parse_args()

    match args.stage:
        case "make-script":
            if not os.path.exists(TRIVIA_INPUT_PATH):
                print(f"Error: Input file {TRIVIA_INPUT_PATH} not found.")
                return
            with open(THEME_INPUT_PATH, "r", encoding="utf-8") as f:
                theme = f.read()
            with open(TRIVIA_INPUT_PATH, "r", encoding="utf-8") as f:
                trivia_text = f.read()
            
            draft_template = read_prompt_template(MAKE_SCRIPT_PROMPT_FILE)
            verify_template = read_prompt_template(MAKE_SCRIPT_VERIFY_PROMPT_FILE)
            res = make_script(theme, trivia_text, draft_template, verify_template)
            save_json(MAKE_SCRIPT_JSON, res.model_dump())

        case "add-char":
            script_data = load_json(MAKE_SCRIPT_JSON)
            prompt_template = read_prompt_template(ADD_CHARACTER_SCRIPT_PROMPT_FILE)
            res = add_character_script(script_data.get("script", ""), prompt_template)
            save_json(ADD_CHARACTER_JSON, res.model_dump())

        case "coeroink":
            char_data = load_json(ADD_CHARACTER_JSON)
            prompt_template = read_prompt_template(OUTPUT_COEROINK_TXT_PROMPT_FILE)
            res = output_coeroink_txt(char_data.get("script", ""), prompt_template)
            save_json(COEROINK_JSON, res.model_dump())

        case "gen-voice":
            combined_audio, words_data = generate_voice_data()
            combined_audio.export(OUTPUT_VOICE, format="wav")
            save_json(VOICE_DATA_JSON, {"words": words_data})
            print(f"  -> Saved voice data to {VOICE_DATA_JSON}")

        case "gen-subtitle":
            voice_data = load_json(VOICE_DATA_JSON)
            print(f"Running gen-subtitle stage...")
            audio_clip = AudioFileClip(OUTPUT_VOICE)
            subtitle_clip = generate_subtitle(voice_data, audio_clip=audio_clip)
            subtitle_clip.write_videofile(OUTPUT_MP4, fps=FPS, codec="libx264", audio_codec="aac")
            print(f"  -> Saved subtitle video to {OUTPUT_MP4}")

        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
