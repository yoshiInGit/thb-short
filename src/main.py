import os
import argparse
from gen_script import make_script, add_character_script, output_coeroink_txt
from generate_voice_data import generate_voice_data
from generate_video import generate_img_request, generate_subtitle
from utils import load_json
from config import MAKE_SCRIPT_JSON, ADD_CHARACTER_JSON, VOICE_DATA_JSON

def gen_script_pipeline():
    """スクリプト生成パイプラインの実行"""
    print("Starting automatic script generation pipeline...")
    
    input_path = "input/trivia.txt"
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return
        
    with open(input_path, "r", encoding="utf-8") as f:
        trivia_text = f.read()
        
    try:
        script_data = make_script(trivia_text)
        char_script_data = add_character_script(script_data)
        output_coeroink_txt(char_script_data)
        print("Pipeline finished successfully!")
    except Exception as e:
        print(f"Error during pipeline execution: {e}")

def main():
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

    args = parser.parse_args()

    if args.command == "gen-script":
        if args.step == "all":
            gen_script_pipeline()
        elif args.step == "make-script":
            input_path = "input/trivia.txt"
            with open(input_path, "r", encoding="utf-8") as f:
                trivia_text = f.read()
            make_script(trivia_text)
        elif args.step == "add-char":
            script_data = load_json(MAKE_SCRIPT_JSON)
            add_character_script(script_data)
        elif args.step == "coeroink":
            char_script_data = load_json(ADD_CHARACTER_JSON)
            output_coeroink_txt(char_script_data)

    elif args.command == "gen-voice":
        generate_voice_data()

    elif args.command == "gen-video":
        if args.step == "gen-img-req":
            voice_data = load_json(VOICE_DATA_JSON)
            generate_img_request(voice_data)
        elif args.step == "gen-sub":
            voice_data = load_json(VOICE_DATA_JSON)
            generate_subtitle(voice_data)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
