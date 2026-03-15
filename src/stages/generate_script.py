import os
from model.script import MakeScriptResponse, AddCharacterScriptResponse, OutputCoeroinkTxtResponse
from util.prompt import load_prompt
from util.gemini import generate_structured_content
from util.file_io import save_json
from config import (
    DEFAULT_MODEL, DEFAULT_TEMPERATURE, COEROINK_TEMPERATURE,
    MAKE_SCRIPT_JSON, ADD_CHARACTER_JSON, COEROINK_JSON, COEROINK_TXT, TRIVIA_INPUT_PATH
)

# ===== Processing Functions =====

def gen_script_pipeline():
    """スクリプト生成パイプラインの実行"""
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

def make_script(trivia_text: str) -> MakeScriptResponse:
    """雑学情報をもとに台本を生成する"""
    print("Running make_script...")
    prompt = load_prompt("make_script.txt", trivia_text=trivia_text)
    
    return generate_structured_content(
        func_name="make_script",
        model=DEFAULT_MODEL,
        prompt=prompt,
        response_schema=MakeScriptResponse,
        temperature=DEFAULT_TEMPERATURE
    )


def add_character_script(script_text: str) -> AddCharacterScriptResponse:
    """台本テキストから、キャラクターの台本を生成する"""
    print("Running add_character_script...")
    prompt = load_prompt("add_character_script.txt", script_text=script_text)
    
    return generate_structured_content(
        func_name="add_character_script",
        model=DEFAULT_MODEL,
        prompt=prompt,
        response_schema=AddCharacterScriptResponse,
        temperature=DEFAULT_TEMPERATURE
    )


def output_coeroink_txt(script_text: str) -> OutputCoeroinkTxtResponse:
    """受け取ったscriptから、文節ごとに改行したテキストデータを作成する"""
    print("Running output_coeroink_txt...")
    prompt = load_prompt("output_coeroink_txt.txt", script_text=script_text)
    
    return generate_structured_content(
        func_name="output_coeroink_txt",
        model=DEFAULT_MODEL,
        prompt=prompt,
        response_schema=OutputCoeroinkTxtResponse,
        temperature=COEROINK_TEMPERATURE
    )

