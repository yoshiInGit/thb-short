import os
import json
import argparse
import string
from datetime import datetime
from google import genai
from google.genai import types
from models import MakeScriptResponse, AddCharacterScriptResponse, OutputCoeroinkTxtResponse

# ===== Constants & Paths =====
OUTPUT_DIR = "output"
PROMPT_DIR = "prompts"
LOG_DIR = "logs"
MAKE_SCRIPT_JSON = os.path.join(OUTPUT_DIR, "make_script.json")
ADD_CHARACTER_JSON = os.path.join(OUTPUT_DIR, "add_character.json")
COEROINK_JSON = os.path.join(OUTPUT_DIR, "coeroink.json")
COEROINK_TXT = os.path.join(OUTPUT_DIR, "coeroink.txt")
IMG_REQUEST_TXT = os.path.join(OUTPUT_DIR, "img_request.txt")

def _load_prompt(filename: str, **kwargs) -> str:
    """外部ファイルからプロンプトを読み込み、変数を埋め込む"""
    path = os.path.join(PROMPT_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        template_str = f.read()
    
    return string.Template(template_str).safe_substitute(**kwargs)

# ===== Processing Functions =====

def _get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")
    return genai.Client(api_key=api_key)


def _save_log(func_name: str, model: str, prompt: str, response: str) -> None:
    """生成結果をログファイルとして保存する"""
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{timestamp}_{func_name}.json"
    log_path = os.path.join(LOG_DIR, log_filename)
    
    log_data = {
        "timestamp": timestamp,
        "function": func_name,
        "model": model,
        "prompt": prompt,
        "response": response
    }
    
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    print(f"  -> Log saved to {log_path}")


def make_script(trivia_text: str) -> dict:
    """雑学情報をもとに台本を生成する"""
    print("Running make_script...")
    client = _get_gemini_client()
    model = "gemini-3.1-flash-lite-preview"
    
    prompt = _load_prompt("make_script.txt", trivia_text=trivia_text)
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MakeScriptResponse,
            temperature=0.7,
        ),
    )
    
    data = json.loads(response.text)
    _save_log("make_script", model, prompt, response.text)
    
    result = {
        "title": data.get("title", ""),
        "script": data.get("script", "")
    }
    
    # 中間データの保存
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(MAKE_SCRIPT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"  -> Saved to {MAKE_SCRIPT_JSON}")
    
    return result


def add_character_script(script_data: dict) -> dict:
    """台本データから、キャラクターの台本を生成する"""
    print("Running add_character_script...")
    client = _get_gemini_client()
    model = "gemini-3.1-flash-lite-preview"
    
    prompt = _load_prompt("add_character_script.txt", script_text=script_data.get("script", ""))
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AddCharacterScriptResponse,
            temperature=0.7,
        ),
    )
    
    data = json.loads(response.text)
    _save_log("add_character_script", model, prompt, response.text)
    
    result = {
        "title": script_data.get("title", ""),
        "script": data.get("script", "")
    }

    # 中間データの保存
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(ADD_CHARACTER_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"  -> Saved to {ADD_CHARACTER_JSON}")

    return result


def output_coeroink_txt(script_data: dict) -> dict:
    """受け取ったscriptから、文節ごとに改行したテキストファイルを出力する"""
    print("Running output_coeroink_txt...")
    client = _get_gemini_client()
    model = "gemini-3.1-flash-lite-preview"
    
    prompt = _load_prompt("output_coeroink_txt.txt", script_text=script_data.get('script', ''))
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=OutputCoeroinkTxtResponse,
            temperature=0.2,
        ),
    )
    
    data = json.loads(response.text)
    _save_log("output_coeroink_txt", model, prompt, response.text)
    
    break_script = data.get("break_script", "")
    
    # テキストファイルの保存
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(COEROINK_TXT, "w", encoding="utf-8") as f:
        f.write(break_script)
    print(f"  -> Saved to {COEROINK_TXT}")
    
    # 中間データの保存 (JSON)
    result = {"break_script": break_script}
    with open(COEROINK_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"  -> Saved to {COEROINK_JSON}")

    return result


def output_img_request(coeroink_data: dict) -> None:
    """必要な画像リストを作成し、ファイルに出力する"""
    print("Running output_img_request...")
    client = _get_gemini_client()
    model = "gemini-3.1-flash-lite-preview"
    
    prompt = _load_prompt("output_img_request.txt", script_text=coeroink_data.get('break_script', ''))
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
        ),
    )
    
    _save_log("output_img_request", model, prompt, response.text)
    
    # テキストファイルの保存
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(IMG_REQUEST_TXT, "w", encoding="utf-8") as f:
        f.write(response.text)
        
    print(f"  -> Saved to {IMG_REQUEST_TXT}")

# 個別処理したいときのために、引数で実行する関数を指定できるようにする
def main():
    parser = argparse.ArgumentParser(description="ショート動画台本生成パイプラインの個別実行ツール")
    parser.add_argument("command", choices=["all", "make_script", "add_char", "coeroink", "img_req"], help="実行するコマンド")
    args = parser.parse_args()

    if args.command == "all":
        # 1. 入力ファイルの読み込み
        input_path = "input/trivia.txt"
        with open(input_path, "r", encoding="utf-8") as f:
            trivia_text = f.read()
        
        script_data = make_script(trivia_text)
        char_script_data = add_character_script(script_data)
        coeroink_data = output_coeroink_txt(char_script_data)
        output_img_request(coeroink_data)
        print("Done.")

    elif args.command == "make_script":
        input_path = "input/trivia.txt"
        with open(input_path, "r", encoding="utf-8") as f:
            trivia_text = f.read()
        make_script(trivia_text)

    elif args.command == "add_char":
        if not os.path.exists(MAKE_SCRIPT_JSON):
            print(f"Error: {MAKE_SCRIPT_JSON} が見つかりません。まず make_script を実行してください。")
            return
        with open(MAKE_SCRIPT_JSON, "r", encoding="utf-8") as f:
            script_data = json.load(f)
        add_character_script(script_data)

    elif args.command == "coeroink":
        if not os.path.exists(ADD_CHARACTER_JSON):
            print(f"Error: {ADD_CHARACTER_JSON} が見つかりません。まず add_char を実行してください。")
            return
        with open(ADD_CHARACTER_JSON, "r", encoding="utf-8") as f:
            char_script_data = json.load(f)
        output_coeroink_txt(char_script_data)

    elif args.command == "img_req":
        if not os.path.exists(COEROINK_JSON):
            print(f"Error: {COEROINK_JSON} が見つかりません。まず coeroink を実行してください。")
            return
        with open(COEROINK_JSON, "r", encoding="utf-8") as f:
            coeroink_data = json.load(f)
        output_img_request(coeroink_data)

if __name__ == "__main__":
    main()

