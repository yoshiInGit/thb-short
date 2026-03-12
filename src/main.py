import os
import argparse
from gen_script import make_script, add_character_script, output_coeroink_txt

def gen_script_pipeline():
    """スクリプト生成パイプラインの実行"""
    print("Starting automatic script generation pipeline...")
    
    # 1. 入力ファイルの読み込み
    input_path = "input/trivia.txt"
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return
        
    with open(input_path, "r", encoding="utf-8") as f:
        trivia_text = f.read()
        
    try:
        # 2. パイプライン処理の実行
        script_data = make_script(trivia_text)
        char_script_data = add_character_script(script_data)
        output_coeroink_txt(char_script_data)
        
        print("Pipeline finished successfully!")
        
    except Exception as e:
        print(f"Error during pipeline execution: {e}")

def main():
    parser = argparse.ArgumentParser(description="THB Short 動画制作支援ツール")
    subparsers = parser.add_subparsers(dest="command", help="実行するコマンド")

    # gen-script コマンドの設定
    subparsers.add_parser("gen-script", help="スクリプト生成パイプラインを実行します")

    args = parser.parse_args()

    if args.command == "gen-script":
        gen_script_pipeline()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
