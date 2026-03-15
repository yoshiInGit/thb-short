import os
from stages.generate_script import make_script, add_character_script, output_coeroink_txt
from util.file_io import save_json
from config import (
    MAKE_SCRIPT_JSON, ADD_CHARACTER_JSON, COEROINK_JSON, COEROINK_TXT, TRIVIA_INPUT_PATH
)

def gen_script_pipeline():
    """台本生成の一連のフローを実行する"""
    print("Starting automatic script generation pipeline...")
    
    if not os.path.exists(TRIVIA_INPUT_PATH):
        print(f"Error: Input file {TRIVIA_INPUT_PATH} not found.")
        return
        
    with open(TRIVIA_INPUT_PATH, "r", encoding="utf-8") as f:
        trivia_text = f.read()
        
    try:
        # 1. Make Script
        script_res = make_script(trivia_text)
        save_json(MAKE_SCRIPT_JSON, script_res.model_dump())

        # 2. Add Character
        char_res = add_character_script(script_res.script)
        save_json(ADD_CHARACTER_JSON, char_res.model_dump())

        # 3. Output Coeroink Txt
        coeroink_res = output_coeroink_txt(char_res.script)
        save_json(COEROINK_JSON, coeroink_res.model_dump())
        
        # テキストファイルの保存
        full_content = f"{script_res.title}\n\n{coeroink_res.break_script}" if script_res.title else coeroink_res.break_script
        with open(COEROINK_TXT, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"  -> Saved text to {COEROINK_TXT}")

        print("Pipeline finished successfully!")
    except Exception as e:
        print(f"Error during pipeline execution: {e}")
