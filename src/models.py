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

class ImgRequestItem(BaseModel):
    time_start: int = Field(description="開始時間(ms)")
    time_end: int = Field(description="終了時間(ms)")
    img_description: str = Field(description="画像を示す単語")

class ImgRequestResponse(BaseModel):
    thinking: str = Field(description="思考過程")
    img_request: list[ImgRequestItem] = Field(description="画像リスト")
