from stages.generate_video import generate_img_request
from util.file_io import load_json, save_json
from config import VOICE_DATA_JSON, IMG_REQUEST_JSON

def gen_img_request_pipeline():
    """画像リクエストの生成フローを実行する"""
    voice_data = load_json(VOICE_DATA_JSON)
    res = generate_img_request(voice_data)
    save_json(IMG_REQUEST_JSON, res.model_dump())
