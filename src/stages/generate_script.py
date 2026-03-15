from model.script import MakeScriptResponse, AddCharacterScriptResponse, OutputCoeroinkTxtResponse
from util.prompt import load_prompt
from util.gemini import generate_structured_content
from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE, COEROINK_TEMPERATURE

# ===== Processing Functions =====

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

