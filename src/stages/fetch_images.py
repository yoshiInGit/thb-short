import os
import requests
from config import PIXABAY_API_KEY, SLIDE_IMGS_DIR, SLIDE_IMGS_JSON
from util.file_io import save_json

def fetch_pixabay_images(img_request_data: dict) -> dict:
    """
    Pixabay APIを使用して画像を検索し、ダウンロードするステージ。
    画像パスと表示タイミングをまとめたメタデータを返す。
    """
    print("Running fetch_pixabay_images...")
    
    os.makedirs(SLIDE_IMGS_DIR, exist_ok=True)
    
    img_requests = img_request_data.get("img_request", [])
    slide_imgs = []
    
    for i, item in enumerate(img_requests):
        query = item.get("img_description", "")
        time_start = item.get("time_start", 0)
        time_end = item.get("time_end", 0)
        
        if not query:
            continue
            
        print(f"  Searching for: {query}")
        
        # Pixabay APIリクエスト
        params = {
            "key": PIXABAY_API_KEY,
            "q": query,
            "image_type": "photo",
            "per_page": 3,
            "orientation": "horizontal",
            "safesearch": "true"
        }
        
        response = requests.get("https://pixabay.com/api/", params=params)
        response.raise_for_status()
        data = response.json()
        
        hits = data.get("hits", [])
        if hits:
            # 最初の1枚を使用
            img_url = hits[0].get("webformatURL")
            img_ext = os.path.splitext(img_url)[1] if img_url else ".jpg" # 拡張子を取得
            img_filename = f"slide_{i:03d}{img_ext}"
            img_path = os.path.join(SLIDE_IMGS_DIR, img_filename)
                
            # 画像のダウンロード
            img_data = requests.get(img_url).content
            with open(img_path, "wb") as f:
                f.write(img_data)
                
            print(f"    -> Downloaded: {img_filename}")
                
            slide_imgs.append({
                "time_start": time_start,
                "time_end": time_end,
                "img_path": img_filename,
                "query": query
            })
        else:
            print(f"    -> No images found for query: {query}")
            # ヒットしなかった場合、直前の画像があればその終了時間を今回の終了時間まで延長する
            if slide_imgs:
                slide_imgs[-1]["time_end"] = time_end
                print(f"    -> Extended previous image duration to {time_end}")
                

    result = {
        "slide_imgs": slide_imgs
    }
    
    return result
