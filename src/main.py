import os
import argparse
from stages.generate_script import make_script, add_character_script, output_coeroink_txt
from pipeline.script_pipeline import gen_script_pipeline
from pipeline.subtitle_pipeline import gen_subtitle_pipeline
from pipeline.video_pipeline import gen_img_request_pipeline
from util.file_io import load_json, save_json
from config import (
    MAKE_SCRIPT_JSON, ADD_CHARACTER_JSON, COEROINK_JSON, TRIVIA_INPUT_PATH
)


def _parse_args():
    """コマンドライン引数の解析"""
    parser = argparse.ArgumentParser(description="THB Short 動画制作支援ツール")
    subparsers = parser.add_subparsers(dest="command", help="実行するコマンド")

    # gen-script コマンド
    script_parser = subparsers.add_parser("gen-script", help="台本生成に関連する操作")
    script_parser.add_argument("step", choices=["all", "make-script", "add-char", "coeroink"], 
                              nargs='?', default="all", help="実行するステップ (default: all)")

    # gen-subtitle コマンド
    subparsers.add_parser("gen-subtitle", help="音声データとメタ情報、字幕動画の生成を実行します")

    # gen-video コマンド
    video_parser = subparsers.add_parser("gen-video", help="動画生成に関連する操作")
    video_parser.add_argument("step", choices=["gen-img-req"], help="実行するステップ")

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

def _handle_gen_subtitle():
    """音声データ生成の処理"""
    gen_subtitle_pipeline()

def _handle_gen_video(args):
    """動画生成に関連する操作の処理"""
    match args.step:
        case "gen-img-req":
            gen_img_request_pipeline()


def main():
    args, parser = _parse_args()

    match args.command:
        case "gen-script":
            _handle_gen_script(args)
            
        case "gen-subtitle":
            _handle_gen_subtitle()
            
        case "gen-video":
            _handle_gen_video(args)
            
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
