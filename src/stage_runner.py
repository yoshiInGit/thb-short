import os
import argparse
from stages.generate_script import make_script, add_character_script, output_coeroink_txt
from stages.generate_slideshow import generate_slideshow
from pipeline.video_pipeline import gen_img_request_pipeline
from util.file_io import load_json, save_json
from config import (
    MAKE_SCRIPT_JSON, ADD_CHARACTER_JSON, COEROINK_JSON, TRIVIA_INPUT_PATH,
    IMG_REQUEST_JSON, SLIDE_IMGS_JSON
)

def _parse_args():
    """コマンドライン引数の解析"""
    parser = argparse.ArgumentParser(description="THB Short 各工程（ステージ）単独実行ツール")
    parser.add_argument("stage", choices=["make-script", "add-char", "coeroink", "gen-img-req", "fetch-images", "gen-slideshow"], help="実行するステージ")
    
    return parser.parse_args(), parser

def main():
    args, parser = _parse_args()

    match args.stage:
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

        case "gen-img-req":
            gen_img_request_pipeline()

        case "fetch-images":
            from stages.fetch_images import fetch_pixabay_images
            img_req_data = load_json(IMG_REQUEST_JSON)
            res = fetch_pixabay_images(img_req_data)
            save_json(SLIDE_IMGS_JSON, res)

        case "gen-slideshow":
            slide_imgs_data = load_json(SLIDE_IMGS_JSON)
            generate_slideshow(slide_imgs_data)

        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
