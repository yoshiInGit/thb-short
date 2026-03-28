from pydantic import BaseModel, Field

# --- 台本生成：1回目出力（初稿）スキーマ ---
class MakeScriptDraftResponse(BaseModel):
    thinking: str = Field(description="初稿の思考過程")
    title: str = Field(description="台本タイトル（初稿）")
    script: str = Field(description="台本の文章（初稿）")

# --- 台本生成：2回目出力（改善版）スキーマ ---
class MakeScriptResponse(BaseModel):
    verification_thinking: str = Field(description="初稿を検証した思考過程")
    title: str = Field(description="台本タイトル（改善版）")
    script: str = Field(description="台本の文章（改善版）")

class AddCharacterScriptResponse(BaseModel):
    thinking: str = Field(description="思考過程")
    script: str = Field(description="キャラクターの台本の文章")

class OutputCoeroinkTxtResponse(BaseModel):
    thinking: str = Field(description="思考過程")
    break_script: str = Field(description="改行された台本の文章")
