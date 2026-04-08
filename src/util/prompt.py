import os
import string
from config import PROMPT_DIR

def read_prompt_template(filename: str) -> str:
    """外部ファイルからプロンプトのテンプレート文字列を読み込む"""
    path = os.path.join(PROMPT_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_prompt(filename: str, **kwargs) -> str:
    """外部ファイルからプロンプトを読み込み、変数を埋め込む"""
    template_str = read_prompt_template(filename)
    return string.Template(template_str).safe_substitute(**kwargs)
