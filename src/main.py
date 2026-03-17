import argparse
from pipeline.script_pipeline import gen_script_pipeline
from pipeline.video_pipeline import gen_video_footage
from pipeline.final_video_pipeline import gen_final_video_pipeline

def _parse_args():
    """コマンドライン引数の解析"""
    parser = argparse.ArgumentParser(description="THB Short 動画制作支援 パイプラインツール")
    subparsers = parser.add_subparsers(dest="command", help="実行するパイプライン")

    # gen-script パイプライン
    subparsers.add_parser("gen-script", help="台本生成に関する一連のパイプラインを実行します")

    # gen-video-footage パイプライン
    subparsers.add_parser("gen-video-footage", help="音声、字幕、画像取得、スライドショー生成の一連のパイプラインを実行します")

    # gen-final-video パイプライン
    subparsers.add_parser("gen-final-video", help="スライドショー＋中央字幕＋音声の最終動画を一括生成します")

    return parser.parse_args(), parser

def main():
    args, parser = _parse_args()

    match args.command:
        case "gen-script":
            gen_script_pipeline()
            
        case "gen-video-footage":
            gen_video_footage()
            
        case "gen-final-video":
            gen_final_video_pipeline()
            
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()

