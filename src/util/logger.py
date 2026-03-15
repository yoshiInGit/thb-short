import os
import json
from datetime import datetime
from config import LOG_DIR

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
