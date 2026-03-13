import os
import json
import argparse
from google.genai import types
from models import MakeScriptResponse, AddCharacterScriptResponse, OutputCoeroinkTxtResponse
from utils import get_gemini_client, load_prompt, save_log, generate_content_with_gemini, save_json, load_json
from config import (
    MAKE_SCRIPT_JSON, ADD_CHARACTER_JSON, COEROINK_JSON, COEROINK_TXT,
    OUTPUT_DIR, DEFAULT_MODEL, DEFAULT_TEMPERATURE, COEROINK_TEMPERATURE
)

# ===== Processing Functions =====

def make_script(trivia_text: str) -> dict:
    """雑学情報をもとに台本を生成する"""
    print("Running make_script...")
    prompt = load_prompt("make_script.txt", trivia_text=trivia_text)
    
    response = generate_content_with_gemini(
        model=DEFAULT_MODEL,
        prompt=prompt,
        response_schema=MakeScriptResponse,
        temperature=DEFAULT_TEMPERATURE
    )
    
    data = json.loads(response.text)
    save_log("make_script", model, prompt, response.text)
    
    result = {
        "title": data.get("title", ""),
        "script": data.get("script", "")
    }
    
    # 中間データの保存
    save_json(MAKE_SCRIPT_JSON, result)
    
    return result


def add_character_script(script_data: dict) -> dict:
    """台本データから、キャラクターの台本を生成する"""
    print("Running add_character_script...")
    prompt = load_prompt("add_character_script.txt", script_text=script_data.get("script", ""))
    
    response = generate_content_with_gemini(
        model=DEFAULT_MODEL,
        prompt=prompt,
        response_schema=AddCharacterScriptResponse,
        temperature=DEFAULT_TEMPERATURE
    )
    
    data = json.loads(response.text)
    save_log("add_character_script", model, prompt, response.text)
    
    result = {
        "title": script_data.get("title", ""),
        "script": data.get("script", "")
    }

    # 中間データの保存
    save_json(ADD_CHARACTER_JSON, result)

    return result


def output_coeroink_txt(script_data: dict) -> dict:
    """受け取ったscriptから、文節ごとに改行したテキストファイルを出力する"""
    print("Running output_coeroink_txt...")
    prompt = load_prompt("output_coeroink_txt.txt", script_text=script_data.get('script', ''))
    
    response = generate_content_with_gemini(
        model=DEFAULT_MODEL,
        prompt=prompt,
        response_schema=OutputCoeroinkTxtResponse,
        temperature=COEROINK_TEMPERATURE
    )
    
    data = json.loads(response.text)
    save_log("output_coeroink_txt", model, prompt, response.text)
    
    break_script = data.get("break_script", "")
    
    # テキストファイルの保存
    title = script_data.get("title", "")
    full_content = f"{title}\n\n{break_script}" if title else break_script
    
    # 出力ディレクトリの作成＆テキストファイルの保存
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(COEROINK_TXT, "w", encoding="utf-8") as f:
        f.write(full_content)
    print(f"  -> Saved to {COEROINK_TXT}")
    
    # 中間データの保存 (JSON)
    result = {"break_script": break_script}
    save_json(COEROINK_JSON, result)

    return result


# 個別処理したいときのために、引数で実行する関数を指定できるようにする
def main():
    parser = argparse.ArgumentParser(description="ショート動画台本生成パイプラインの個別実行ツール")
    parser.add_argument("command", choices=["all", "make_script", "add_char", "coeroink"], help="実行するコマンド")
    args = parser.parse_args()

    if args.command == "all":
        # 1. 入力ファイルの読み込み
        input_path = "input/trivia.txt"
        with open(input_path, "r", encoding="utf-8") as f:
            trivia_text = f.read()
        
        script_data = make_script(trivia_text)
        char_script_data = add_character_script(script_data)
        coeroink_data = output_coeroink_txt(char_script_data)
        print("Done."+coeroink_data.get("break_script", ""))

    elif args.command == "make_script":
        input_path = "input/trivia.txt"
        with open(input_path, "r", encoding="utf-8") as f:
            trivia_text = f.read()
        make_script(trivia_text)

    elif args.command == "add_char":
        script_data = load_json(MAKE_SCRIPT_JSON)
        add_character_script(script_data)

    elif args.command == "coeroink":
        char_script_data = load_json(ADD_CHARACTER_JSON)
        output_coeroink_txt(char_script_data)

if __name__ == "__main__":
    main()

