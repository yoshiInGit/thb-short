import json
import os
from pydantic import BaseModel

class DummyResponse:
    """Gemini APIのレスポンスを模倣するクラス"""
    def __init__(self, data):
        self.text = json.dumps(data, ensure_ascii=False)

SCHEMA_TO_FILE = {
    "MakeScriptResponse": "make_script.json",
    "AddCharacterScriptResponse": "add_character.json",
    "OutputCoeroinkTxtResponse": "coeroink.json",
    "ImgRequestResponse": "img_request.json",
    "VoiceData": "voice_data.json"
}

def _generate_dummy_data(response_schema: type[BaseModel]) -> dict:
    """src/dummy内のファイル、またはスキーマに基づいてダミーデータを生成する"""
    # スキーマ名に対応するダミーファイルを探す
    dummy_dir = os.path.dirname(__file__)
    schema_name = response_schema.__name__
    
    if schema_name not in SCHEMA_TO_FILE:
        raise ValueError(f"Unknown schema: {schema_name}")

    file_path = os.path.join(dummy_dir, SCHEMA_TO_FILE[schema_name])
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dummy file not found: {file_path}")

    print(f"  [MOCK] Loading dummy data from {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
