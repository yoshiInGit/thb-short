import os
from stages.generate_script import make_script, output_coeroink_txt
from util.file_io import save_json
from util.prompt import read_prompt_template
from config import (
    MAKE_SCRIPT_JSON, COEROINK_JSON, COEROINK_TXT, TRIVIA_INPUT_PATH, THEME_INPUT_PATH,
    MAKE_SCRIPT_PROMPT_FILE, MAKE_SCRIPT_VERIFY_PROMPT_FILE,
    OUTPUT_COEROINK_TXT_PROMPT_FILE
)

def gen_script_pipeline():
    """台本生成の一連のフローを実行する"""
    print("Starting automatic script generation pipeline...")

        
    with open(THEME_INPUT_PATH, "r", encoding="utf-8") as f:
        theme = f.read()
        
    with open(TRIVIA_INPUT_PATH, "r", encoding="utf-8") as f:
        trivia_text = f.read()
        
    # プロンプトテンプレートの読み込み
    draft_template    = read_prompt_template(MAKE_SCRIPT_PROMPT_FILE)
    verify_template   = read_prompt_template(MAKE_SCRIPT_VERIFY_PROMPT_FILE)
    coeroink_template = read_prompt_template(OUTPUT_COEROINK_TXT_PROMPT_FILE)

    # 1. Make Script
    script_res = make_script(theme, trivia_text, draft_template, verify_template)
    save_json(MAKE_SCRIPT_JSON, script_res.model_dump())

    # 2. Output Coeroink Txt
    coeroink_res = output_coeroink_txt(script_res.script, coeroink_template)
    save_json(COEROINK_JSON, coeroink_res.model_dump())
    
    # 保存用テキストの構築（タイトルがある場合は冒頭に追加）
    full_content = f"{script_res.title}\n\n{coeroink_res.break_script}"
    
    
    with open(COEROINK_TXT, "w", encoding="utf-8") as f:
        f.write(full_content)
    
    print(f"  -> Saved text to {COEROINK_TXT}")

    print("Pipeline finished successfully!")
