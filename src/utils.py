import os
import json
import string
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from dummy.mock import DummyResponse, _generate_dummy_data
from config import LOG_DIR, PROMPT_DIR

# 環境変数の読み込み
load_dotenv()

def find_file(*paths):
    """複数のパスからファイルを探し、最初に見つかったパスを返す"""
    for p in paths:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"File not found. Checked: {paths}")

def get_gemini_client():
    """Gemini APIクライアントを初期化して返す"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")
    return genai.Client(api_key=api_key)

def load_prompt(filename: str, **kwargs) -> str:
    """外部ファイルからプロンプトを読み込み、変数を埋め込む"""
    
    # src/からの相対パスまたはカレントからの相対パスを試行
    base_path = os.path.dirname(__file__)
    path = find_file(
        os.path.join(base_path, PROMPT_DIR, filename),
        os.path.join(PROMPT_DIR, filename)
    )
    
    # プロンプトファイルを読み込む
    with open(path, "r", encoding="utf-8") as f:
        template_str = f.read()
    
    return string.Template(template_str).safe_substitute(**kwargs)

def save_log(func_name: str, model_name: str, prompt: str, response_text: str) -> None:
    """生成結果をログファイルとして保存する"""
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{timestamp}_{func_name}.json"
    log_path = os.path.join(LOG_DIR, log_filename)
    
    log_data = {
        "timestamp": timestamp,
        "function": func_name,
        "model": model_name,
        "prompt": prompt,
        "response": response_text
    }
    
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    print(f"  -> Log saved to {log_path}")

def save_json(path: str, data: any) -> None:
    """JSONデータをファイルに保存する（ディレクトリ作成とメッセージ出力を含む）"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  -> Saved to {path}")

def load_json(path: str) -> any:
    """JSONファイルを読み込む"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"JSON file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

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
    
    # ログの保存（副作用だが、共通化のためここで実行）
    save_log(func_name, model, prompt, response.text)
    
    return result
