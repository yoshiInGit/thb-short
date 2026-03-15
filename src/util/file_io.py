import os
import json

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
