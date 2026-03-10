import os
import json
from google import genai
from google.genai import types
from .models import MakeScriptResponse, AddCharacterScriptResponse, OutputCoeroikTxtResponse

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
    return {
        "title": data.get("title", ""),
        "script": data.get("script", "")
    }


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
    return {
        "title": script_data.get("title", ""),
        "script": data.get("script", "")
    }


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
    
    output_path = "src/output/coeroik.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(break_script)
        
    print(f"  -> Saved to {output_path}")
    return {"break_script": break_script}


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
    
    output_path = "src/output/img_request.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)
        
    print(f"  -> Saved to {output_path}")
