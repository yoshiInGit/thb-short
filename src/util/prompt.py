import os
import string
from config import PROMPT_DIR

def load_prompt(filename: str, **kwargs) -> str:
    """外部ファイルからプロンプトを読み込み、変数を埋め込む"""
    path = os.path.join(PROMPT_DIR, filename)
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")
    
    # プロンプトファイルを読み込む
    with open(path, "r", encoding="utf-8") as f:
        template_str = f.read()
    
    return string.Template(template_str).safe_substitute(**kwargs)
