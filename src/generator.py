import os
import json
import argparse
from google import genai
from google.genai import types
from .models import MakeScriptResponse, AddCharacterScriptResponse, OutputCoeroikTxtResponse

# ===== Constants & Paths =====
OUTPUT_DIR = "src/output"
MAKE_SCRIPT_JSON = os.path.join(OUTPUT_DIR, "make_script.json")
ADD_CHARACTER_JSON = os.path.join(OUTPUT_DIR, "add_character.json")
COEROIK_JSON = os.path.join(OUTPUT_DIR, "coeroik.json")
COEROIK_TXT = os.path.join(OUTPUT_DIR, "coeroik.txt")
IMG_REQUEST_TXT = os.path.join(OUTPUT_DIR, "img_request.txt")

# ===== Processing Functions =====

def _get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")
    return genai.Client(api_key=api_key)


def make_script(trivia_text: str) -> dict:
    """雑学情報をもとに台本を生成する"""
    print("Running make_script...")
    client = _get_gemini_client()
    model = "gemini-2.0-flashcards"
    
    prompt = f"""
    以下の雑学情報をもとに、ショート動画用の台本を作成してください。
    
    【雑学情報】
    {trivia_text}
    """
    
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
    model = "gemini-2.0-flashcards"
    
    prompt = f"""
    以下の台本を、キャラクター（例：ずんだもん）が話すような口調の台本に変換してください。
    
    【元の台本】
    {json.dumps(script_data, ensure_ascii=False)}
    """
    
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


def output_coeroik_txt(script_data: dict) -> dict:
    """受け取ったscriptから、文節ごとに改行したテキストファイルを出力する"""
    print("Running output_coeroik_txt...")
    client = _get_gemini_client()
    model = "gemini-2.0-flashcards"
    
    prompt = f"""
    以下のキャラクター台本を、音声読み上げソフト（COEIROINK）用に、
    読みやすい文節や息継ぎのタイミングごとに改行を入れてください。
    
    【キャラクター台本】
    {script_data.get('script', '')}
    """
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=OutputCoeroikTxtResponse,
            temperature=0.2,
        ),
    )
    
    data = json.loads(response.text)
    break_script = data.get("break_script", "")
    
    # テキストファイルの保存
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(COEROIK_TXT, "w", encoding="utf-8") as f:
        f.write(break_script)
    print(f"  -> Saved to {COEROIK_TXT}")
    
    # 中間データの保存 (JSON)
    result = {"break_script": break_script}
    with open(COEROIK_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"  -> Saved to {COEROIK_JSON}")

    return result


def output_img_request(coeroik_data: dict) -> None:
    """必要な画像リストを作成し、ファイルに出力する"""
    print("Running output_img_request...")
    client = _get_gemini_client()
    model = "gemini-2.0-flashcards"
    
    prompt = f"""
    以下の台本テキストをもとに、動画編集で必要になるであろう画像のリストを箇条書きで作成してください。
    
    【台本】
    {coeroik_data.get('break_script', '')}
    """
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
        ),
    )
    
    # テキストファイルの保存
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(IMG_REQUEST_TXT, "w", encoding="utf-8") as f:
        f.write(response.text)
        
    print(f"  -> Saved to {IMG_REQUEST_TXT}")

# 個別処理したいときのために、引数で実行する関数を指定できるようにする
def main():
    parser = argparse.ArgumentParser(description="ショート動画台本生成パイプラインの個別実行ツール")
    parser.add_argument("command", choices=["all", "make_script", "add_char", "coeroik", "img_req"], help="実行するコマンド")
    args = parser.parse_args()

    if args.command == "all":
        # 1. 入力ファイルの読み込み
        input_path = "src/input/trivia.txt"
        with open(input_path, "r", encoding="utf-8") as f:
            trivia_text = f.read()
        
        script_data = make_script(trivia_text)
        char_script_data = add_character_script(script_data)
        coeroik_data = output_coeroik_txt(char_script_data)
        output_img_request(coeroik_data)
        print("Done.")

    elif args.command == "make_script":
        input_path = "src/input/trivia.txt"
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

    elif args.command == "coeroik":
        if not os.path.exists(ADD_CHARACTER_JSON):
            print(f"Error: {ADD_CHARACTER_JSON} が見つかりません。まず add_char を実行してください。")
            return
        with open(ADD_CHARACTER_JSON, "r", encoding="utf-8") as f:
            char_script_data = json.load(f)
        output_coeroik_txt(char_script_data)

    elif args.command == "img_req":
        if not os.path.exists(COEROIK_JSON):
            print(f"Error: {COEROIK_JSON} が見つかりません。まず coeroik を実行してください。")
            return
        with open(COEROIK_JSON, "r", encoding="utf-8") as f:
            coeroik_data = json.load(f)
        output_img_request(coeroik_data)

if __name__ == "__main__":
    main()

