import json
import argparse
from google.genai import types
from models import ImgRequestResponse
from utils import load_prompt, save_log, generate_content_with_gemini, save_json, load_json
from config import VOICE_DATA_JSON, IMG_REQUEST_JSON, DEFAULT_MODEL, DEFAULT_TEMPERATURE

def generate_img_request(voice_data: dict) -> dict:
    """音声データをもとに、Geminiで画像リクエストを生成する"""
    print("Running generate_img_request...")
    
    # プロンプトの準備
    # voice_dataを文字列化して渡す
    voice_data_str = json.dumps(voice_data, ensure_ascii=False, indent=2)
    prompt = load_prompt("generate_img_request.txt", voice_data=voice_data_str)
    
    response = generate_content_with_gemini(
        model=DEFAULT_MODEL,
        prompt=prompt,
        response_schema=ImgRequestResponse,
        temperature=DEFAULT_TEMPERATURE
    )
    
    data = json.loads(response.text)
    save_log("generate_img_request", model, prompt, response.text)
    
    # 中間データの保存
    save_json(IMG_REQUEST_JSON, data)
    
    return data

def main():
    parser = argparse.ArgumentParser(description="動画生成支援ツール")
    parser.add_argument("command", choices=["gen-img-req"], help="実行するコマンド")
    args = parser.parse_args()

    if args.command == "gen-img-req":
        voice_data = load_json(VOICE_DATA_JSON)
        generate_img_request(voice_data)

if __name__ == "__main__":
    main()
