from pydantic import BaseModel, Field

# ===== Pydantic Models for Structured Output =====

class MakeScriptResponse(BaseModel):
    thinking: str = Field(description="思考過程")
    title: str = Field(description="台本タイトル")
    script: str = Field(description="台本の文章")

class AddCharacterScriptResponse(BaseModel):
    thinking: str = Field(description="思考過程")
    script: str = Field(description="キャラクターの台本の文章")

class OutputCoeroinkTxtResponse(BaseModel):
    thinking: str = Field(description="思考過程")
    break_script: str = Field(description="改行された台本の文章")
