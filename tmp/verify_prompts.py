import sys
import os

# src ディレクトリをパスに追加
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    from config import MAKE_SCRIPT_PROMPT_FILE, PROMPT_DIR
    from util.prompt import load_prompt
    
    print(f"PROMPT_DIR: {PROMPT_DIR}")
    print(f"MAKE_SCRIPT_PROMPT_FILE: {MAKE_SCRIPT_PROMPT_FILE}")
    
    # ダミーデータでプロンプトをロード
    prompt = load_prompt(MAKE_SCRIPT_PROMPT_FILE, trivia_text="テスト用の雑学")
    
    print("\n--- Loaded Prompt Snippet (First 100 chars) ---")
    print(prompt[:100])
    print("------------------------------------------\n")
    
    if len(prompt) > 0:
        print("Successfully loaded the prompt from the configured file.")
    else:
        print("Failed: Prompt is empty.")

except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
