import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from dummy.mock import DummyResponse, _generate_dummy_data
from util.logger import save_log

# 環境変数の読み込み
load_dotenv()

def get_gemini_client():
    """Gemini APIクライアントを初期化して返す"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")
    return genai.Client(api_key=api_key)

def generate_content_with_gemini(model: str, prompt: str, response_schema: type[BaseModel], temperature: float = 0.7):
    """Gemini APIを呼び出す。USE_DUMMY_GEMINI=trueの場合はダミーデータを返す。"""
    
    use_dummy = os.environ.get("USE_DUMMY_GEMINI", "false").lower() == "true"

    if not use_dummy:
        client = get_gemini_client()
        return client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema,
                temperature=temperature,
            ),
        )
    else:
        print(f"  [MOCK] Generating dummy response for {response_schema.__name__}...")
        dummy_data = _generate_dummy_data(response_schema)
        return DummyResponse(dummy_data)

def generate_structured_content(func_name: str, model: str, prompt: str, response_schema: type[BaseModel], temperature: float = 0.7) -> BaseModel:
    """共通の生成フロー（API呼び出し -> バリデーション -> ログ保存）を実行する"""
    response = generate_content_with_gemini(
        model=model,
        prompt=prompt,
        response_schema=response_schema,
        temperature=temperature
    )
    
    # Pydanticモデルとしてパース
    result = response_schema.model_validate_json(response.text)
    
    # ログの保存
    save_log(func_name, model, prompt, response.text)
    
    return result
