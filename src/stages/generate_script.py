import string
from model.script import MakeScriptResponse, MakeScriptDraftResponse, AddCharacterScriptResponse, OutputCoeroinkTxtResponse
from util.gemini import generate_structured_content
from config import (
    DEFAULT_MODEL, DEFAULT_TEMPERATURE, COEROINK_TEMPERATURE
)

# ===== Processing Functions =====

def make_script(trivia_text: str, draft_prompt_template: str, verify_prompt_template: str) -> MakeScriptResponse:
    """雑学情報をもとに台本を生成する（2段階：初稿生成→検証・改善）"""
    print("Running make_script...")

    # --- 1回目: Thinking + 初稿出力 ---
    print("  [1/2] 初稿を生成中...")
    draft_prompt = string.Template(draft_prompt_template).safe_substitute(trivia_text=trivia_text)
    draft: MakeScriptDraftResponse = generate_structured_content(
        func_name="make_script_draft",
        model=DEFAULT_MODEL,
        prompt=draft_prompt,
        response_schema=MakeScriptDraftResponse,
        temperature=DEFAULT_TEMPERATURE
    )
    print(f"  [1/2] 初稿Thinking: {draft.thinking[:80]}...")
    print(f"  [1/2] 初稿タイトル: {draft.title}")

    # --- 2回目: 検証Thinking + 改善版出力 ---
    print("  [2/2] 初稿を検証・改善中...")
    verify_prompt = string.Template(verify_prompt_template).safe_substitute(
        draft_title=draft.title,
        draft_script=draft.script
    )
    final: MakeScriptResponse = generate_structured_content(
        func_name="make_script",
        model=DEFAULT_MODEL,
        prompt=verify_prompt,
        response_schema=MakeScriptResponse,
        temperature=DEFAULT_TEMPERATURE
    )
    print(f"  [2/2] 検証Thinking: {final.verification_thinking[:80]}...")
    print(f"  [2/2] 最終タイトル: {final.title}")

    return final


def add_character_script(script_text: str, prompt_template: str) -> AddCharacterScriptResponse:
    """台本テキストから、キャラクターの台本を生成する"""
    print("Running add_character_script...")
    prompt = string.Template(prompt_template).safe_substitute(script_text=script_text)
    
    return generate_structured_content(
        func_name="add_character_script",
        model=DEFAULT_MODEL,
        prompt=prompt,
        response_schema=AddCharacterScriptResponse,
        temperature=DEFAULT_TEMPERATURE
    )


def output_coeroink_txt(script_text: str, prompt_template: str) -> OutputCoeroinkTxtResponse:
    """受け取ったscriptから、文節ごとに改行したテキストデータを作成する"""
    print("Running output_coeroink_txt...")
    prompt = string.Template(prompt_template).safe_substitute(script_text=script_text)
    
    return generate_structured_content(
        func_name="output_coeroink_txt",
        model=DEFAULT_MODEL,
        prompt=prompt,
        response_schema=OutputCoeroinkTxtResponse,
        temperature=COEROINK_TEMPERATURE
    )

