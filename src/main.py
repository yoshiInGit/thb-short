import argparse
from pipeline.script_pipeline import gen_script_pipeline
from pipeline.subtitle_pipeline import gen_subtitle_pipeline

def _parse_args():
    """コマンドライン引数の解析"""
    parser = argparse.ArgumentParser(description="THB Short 動画制作支援 パイプラインツール")
    subparsers = parser.add_subparsers(dest="command", help="実行するパイプライン")

    # gen-script パイプライン
    subparsers.add_parser("gen-script", help="台本生成に関する一連のパイプラインを実行します")

    # gen-subtitle パイプライン
    subparsers.add_parser("gen-subtitle", help="音声データとメタ情報、字幕動画の生成パイプラインを実行します")

    return parser.parse_args(), parser

def main():
    args, parser = _parse_args()

    match args.command:
        case "gen-script":
            gen_script_pipeline()
            
        case "gen-subtitle":
            gen_subtitle_pipeline()
            
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()

