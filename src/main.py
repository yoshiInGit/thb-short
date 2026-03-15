import os
import argparse
from pipelines.generate_script import make_script, add_character_script, output_coeroink_txt, gen_script_pipeline
from pipelines.generate_voice_data import generate_voice_data
from pipelines.generate_video import generate_img_request, generate_subtitle
from util.file_io import load_json, save_json
from config import (
    MAKE_SCRIPT_JSON, ADD_CHARACTER_JSON, COEROINK_JSON, 
    VOICE_DATA_JSON, IMG_REQUEST_JSON, COEROINK_TXT,
    OUTPUT_VOICE, OUTPUT_MP4, FPS, TRIVIA_INPUT_PATH
)


def _parse_args():
    """コマンドライン引数の解析"""
    parser = argparse.ArgumentParser(description="THB Short 動画制作支援ツール")
    subparsers = parser.add_subparsers(dest="command", help="実行するコマンド")

    # gen-script コマンド
    script_parser = subparsers.add_parser("gen-script", help="台本生成に関連する操作")
    script_parser.add_argument("step", choices=["all", "make-script", "add-char", "coeroink"], 
                              nargs='?', default="all", help="実行するステップ (default: all)")

    # gen-voice コマンド
    subparsers.add_parser("gen-voice", help="音声データとメタ情報の生成を実行します")

    # gen-video コマンド
    video_parser = subparsers.add_parser("gen-video", help="動画生成に関連する操作")
    video_parser.add_argument("step", choices=["gen-img-req", "gen-sub"], help="実行するステップ")

    return parser.parse_args(), parser

def _handle_gen_script(args):
    """台本生成に関連する操作の処理"""
    match args.step:
        case "all":
            gen_script_pipeline()

        case "make-script":
            if not os.path.exists(TRIVIA_INPUT_PATH):
                print(f"Error: Input file {TRIVIA_INPUT_PATH} not found.")
                return
            with open(TRIVIA_INPUT_PATH, "r", encoding="utf-8") as f:
                trivia_text = f.read()
            res = make_script(trivia_text)
            save_json(MAKE_SCRIPT_JSON, res.model_dump())

        case "add-char":
            script_data = load_json(MAKE_SCRIPT_JSON)
            res = add_character_script(script_data.get("script", ""))
            save_json(ADD_CHARACTER_JSON, res.model_dump())

        case "coeroink":
            char_data = load_json(ADD_CHARACTER_JSON)
            res = output_coeroink_txt(char_data.get("script", ""))
            save_json(COEROINK_JSON, res.model_dump())

def _handle_gen_voice():
    """音声データ生成の処理"""
    combined_audio, words_data = generate_voice_data()

    # 音声の保存
    combined_audio.export(OUTPUT_VOICE, format="wav")
    print(f"  -> Saved combined voice to {OUTPUT_VOICE}")

    # メタデータの保存
    save_json(VOICE_DATA_JSON, {"words": words_data})

def _handle_gen_video(args):
    """動画生成に関連する操作の処理"""
    match args.step:
        case "gen-img-req":
            voice_data = load_json(VOICE_DATA_JSON)
            res = generate_img_request(voice_data)
            save_json(IMG_REQUEST_JSON, res.model_dump())

        case "gen-sub":
            voice_data = load_json(VOICE_DATA_JSON)
            video_clip = generate_subtitle(voice_data)
            
            print(f"Exporting video to {OUTPUT_MP4}...")
            video_clip.write_videofile(OUTPUT_MP4, fps=FPS, codec="libx264", audio=False)
            print("Export complete!")


def main():
    args, parser = _parse_args()

    match args.command:
        case "gen-script":
            _handle_gen_script(args)
            
        case "gen-voice":
            _handle_gen_voice()
            
        case "gen-video":
            _handle_gen_video(args)
            
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
