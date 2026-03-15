from pydantic import BaseModel, Field

class ImgRequestItem(BaseModel):
    time_start: int = Field(description="開始時間(ms)")
    time_end: int = Field(description="終了時間(ms)")
    img_description: str = Field(description="画像を示す単語")

class ImgRequestResponse(BaseModel):
    thinking: str = Field(description="思考過程")
    img_request: list[ImgRequestItem] = Field(description="画像リスト")
