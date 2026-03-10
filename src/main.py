import os
from .generator import make_script, add_character_script, output_coeroik_txt, output_img_request

def main():
    print("Starting automatic script generation pipeline...")
    
    # 1. 入力ファイルの読み込み
    input_path = "src/input/trivia.txt"
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return
        
    with open(input_path, "r", encoding="utf-8") as f:
        trivia_text = f.read()
        
    try:
        # 2. パイプライン処理の実行
        script_data = make_script(trivia_text)
        char_script_data = add_character_script(script_data)
        coeroik_data = output_coeroik_txt(char_script_data)
        output_img_request(coeroik_data)
        
        print("Pipeline finished successfully!")
        
    except Exception as e:
        print(f"Error during pipeline execution: {e}")

if __name__ == "__main__":
    main()
