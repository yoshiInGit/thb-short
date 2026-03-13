import os
import json
import argparse
import string
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from models import ImgRequestResponse

# ===== Constants & Paths =====
load_dotenv()
OUTPUT_DIR = "output"
INTERMEDIATE_DIR = os.path.join(OUTPUT_DIR, "intermediate")
PROMPT_DIR = "prompts"
LOG_DIR = "logs"
VOICE_DATA_JSON = os.path.join(INTERMEDIATE_DIR, "voice_data.json")
IMG_REQUEST_JSON = os.path.join(INTERMEDIATE_DIR, "img_request.json")

def _get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")
    return genai.Client(api_key=api_key)

def _load_prompt(filename: str, **kwargs) -> str:
    """外部ファイルからプロンプトを読み込み、変数を埋め込む"""
    # src/からの相対パスまたは絶対パスを考慮
    base_path = os.path.dirname(__file__)
    path = os.path.join(base_path, PROMPT_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        template_str = f.read()
    
    return string.Template(template_str).safe_substitute(**kwargs)

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

def generate_img_request(voice_data: dict) -> dict:
    """音声データをもとに、Geminiで画像リクエストを生成する"""
    print("Running generate_img_request...")
    client = _get_gemini_client()
    model = "gemini-3.1-flash-lite-preview"
    
    # プロンプトの準備
    # voice_dataを文字列化して渡す
    voice_data_str = json.dumps(voice_data, ensure_ascii=False, indent=2)
    prompt = _load_prompt("generate_img_request.txt", voice_data=voice_data_str)
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ImgRequestResponse,
            temperature=0.7,
        ),
    )
    
    data = json.loads(response.text)
    _save_log("generate_img_request", model, prompt, response.text)
    
    # 中間データの保存
    os.makedirs(os.path.dirname(IMG_REQUEST_JSON), exist_ok=True)
    with open(IMG_REQUEST_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  -> Saved to {IMG_REQUEST_JSON}")
    
    return data

def main():
    parser = argparse.ArgumentParser(description="動画生成支援ツール")
    parser.add_argument("command", choices=["gen-img-req"], help="実行するコマンド")
    args = parser.parse_args()

    if args.command == "gen-img-req":
        if not os.path.exists(VOICE_DATA_JSON):
            print(f"Error: {VOICE_DATA_JSON} が見つかりません。")
            return
            
        with open(VOICE_DATA_JSON, "r", encoding="utf-8") as f:
            voice_data = json.load(f)
            
        generate_img_request(voice_data)

if __name__ == "__main__":
    main()
