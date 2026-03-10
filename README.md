# 雑学ショート動画台本生成器 (Trivia Short Script Generator)

雑学テキストを元に、ショート動画制作に必要な台本や素材リストを Gemini API (Gemini 2.0 Flash) を活用して自動生成するツールです。

---

## 🚀 主な機能 (Key Features)

1.  **台本生成 (make_script)**: 雑学テキストから動画用のタイトルと基本台本を生成します。
2.  **キャラクター変換 (add_character_script)**: 台本を指定のキャラクター口調（例：ずんだもん）に変換します。
3.  **COEIROINK形式出力 (output_coeroik_txt)**: 音声合成ソフトでの読み上げ用に、文節ごとに改行を入れたテキストファイルを出力します。
4.  **画像リクエスト作成 (output_img_request)**: 台本内容に基づき、動画編集で必要となる画像のリストを書き出します。

## 🛠 使用技術 (Tech Stack)

| カテゴリ           | 技術                                         |
| :----------------- | :------------------------------------------- |
| **Language**       | Python 3.12 (slim)                           |
| **AI Model**       | Gemini 2.0 Flash (`gemini-2.0-flash-exp` 等) |
| **API Library**    | google-genai, pydantic                       |
| **Infrastructure** | Docker, Docker Compose                       |

## 🏁 はじめに (Getting Started)

### 前提条件 (Prerequisites)

- Docker / Docker Compose
- Gemini API Key

### セットアップ (Installation)

1.  **環境変数の設定**:
    プロジェクトルートに `.env` ファイルを作成し、APIキーを設定してください。

    ```text
    GEMINI_API_KEY=your_api_key_here
    ```

2.  **入力データの準備**:
    `src/input/trivia.txt` に、台本の元となる雑学テキストを記入します。

## 📖 使い方 (Usage)

Docker Composeを利用してパイプラインを実行します。

### 実行コマンド

```bash
docker-compose up --build
```

実行後、以下のファイルが生成されます：

- `src/output/coeroik.txt`: 改行済み台本テキスト
- `src/output/img_request.txt`: 必要な画像リスト

### コンテナ内での操作

```bash
# コンテナの中に入って直接実行する場合
docker-compose exec app bash
python src/main.py
```

## 📂 ディレクトリ構成 (Directory Structure)

```text
.
├── src/
│   ├── main.py          # 実行エントリーポイント（パイプライン制御）
│   ├── generator.py     # Gemini API を用いた生成ロジック
│   ├── models.py        # Pydantic によるデータ構造定義
│   ├── input/           # 入力データ
│   │   └── trivia.txt   # 元ネタとなる雑学テキスト
│   └── output/          # 出力データ
│       ├── coeroik.txt  # 読み上げ用テキスト
│       └── img_request.txt # 画像リスト
├── Dockerfile           # Python環境定義
├── docker-compose.yml   # 開発環境設定
├── requirements.txt     # Python依存パッケージ
└── .env                 # 環境変数（Git非推奨）
```
