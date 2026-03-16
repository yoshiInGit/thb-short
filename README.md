# 雑学ショート動画台本生成器 (Trivia Short Script Generator)

雑学テキストを元に、ショート動画制作に必要な台本や素材リストを Gemini API (Gemini 2.0 Flash) を活用して自動生成するツールです。

---

## 🚀 主な機能 (Key Features)

1.  **台本生成 (make_script)**: 雑学テキストから動画用のタイトルと基本台本を生成します。
2.  **キャラクター変換 (add_character_script)**: 台本を指定のキャラクター口調（例：ずんだもん）に変換します。
3.  **COEIROINK形式出力 (output_coeroink_txt)**: 音声合成ソフトでの読み上げ用に、文節ごとに改行を入れたテキストファイルを出力します。
4.  **画像リクエスト作成 (generate_img_request)**: 台本内容に基づき、動画編集で必要となる画像のリストを書き出します。
5.  **画像取得 (fetch_images)**: 画像リクエストに基づき、Pixabay 等から素材画像を自動取得します。
6.  **スライドショー生成 (generate_slideshow)**: 取得した画像と音声タイミングを合わせ、フェード効果付きのスライドショー動画を生成します。

## 🛠 使用技術 (Tech Stack)

| カテゴリ           | 技術                                                  |
| :----------------- | :---------------------------------------------------- |
| **Language**       | Python 3.12 (slim)                                    |
| **AI Model**       | Gemini 2.0 Flash (`gemini-2.0-flash-exp` 等)          |
| **Libraries**      | google-genai, pydantic, python-dotenv, pydub, moviepy |
| **Infrastructure** | Docker, Docker Compose                                |

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

- `src/output/coeroink.txt`: 改行済み台本テキスト
- `src/output/img_request.txt`: 必要な画像リスト

### コンテナ内での操作

```bash
# コンテナの中に入って直接実行する場合
docker-compose exec app bash
python src/main.py [コマンド]
```

### パイプライン実行 (`src/main.py`)

一連の自動化フロー（パイプライン）を実行するためのメインスクリプトです。

| コマンド       | 説明                                                                                                                                                                  |
| :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gen-script`        | 雑学テキストの読み込みから、ベース台本生成、キャラクター口調変換、COEIROINK形式出力までの全ステップを連続で実行します。                                               |
| `gen-video-footage` | 音声データ生成、字幕動画作成、画像リクエスト生成、画像取得、スライドショー生成までの一連の動画素材作成パイプラインを実行します。 |

### 個別ステージ実行 (`src/stage_runner.py`)

各処理（ステージ）を単独で個別に実行・テストするための手動実行用スクリプトです。

```bash
# 台本作成のみ実行
python src/stage_runner.py make-script

# 画像取得のみ実行
python src/stage_runner.py fetch-images

# スライドショー生成のみ実行
python src/stage_runner.py gen-slideshow
```

| 引数 (ステージ) | 説明 |
| :--- | :--- |
| `make-script`   | 入力テキスト(`src/data/input/trivia.txt`)からベースとなる台本(`make_script.json`)のみを生成します。 |
| `add-char`     | 既存の台本データ(`make_script.json`)を元に、キャラクター口調の台本(`add_character.json`)のみに変換します。 |
| `coeroink`     | 既存のキャラクター台本データ(`add_character.json`)を元に、COEIROINK用テキストが出力されます。 |
| `gen-img-req`  | 音声のメタデータ(`voice_data.json`)をもとに、画像リクエストJSONをGeminiで生成します。 |
| `fetch-images` | 画像リクエスト(`img_request.json`)をもとに、Pixabayから画像をダウンロードし、画像リスト(`slide_imgs.json`)を生成します。 |
| `gen-slideshow`| 画像リスト(`slide_imgs.json`)をもとに、スライドショー動画(`slides.mp4`)を生成します。 |

## 📂 ディレクトリ構成 (Directory Structure)

```text
.
├── src/
│   ├── main.py          # 実行エントリーポイント (CLI、各パイプラインの呼び出し)
│   ├── config.py        # パスやモデル設定などの全体定数
│   ├── pipeline/        # 一連の自動化フロー（オーケストレーション）
│   ├── stages/          # アトミックな各処理の実行単位（API通信、動画編集など）
│   ├── util/            # アプリ内共通機能（ロギング、ファイルIO、Geminiクライアント）
│   ├── model/           # Pydantic によるデータ構造定義 (レスポンス型など)
│   ├── data/            # 入力データおよび出力結果
│   ├── logs/            # Gemini API呼び出し時のプロンプトとレスポンスのログ
│   └── prompts/         # Gemini用プロンプトのテンプレート
├── Dockerfile           # Python環境定義
├── docker-compose.yml   # 開発環境設定
├── requirements.txt     # Python依存パッケージ
└── .env                 # 環境変数
```

### コンポーネント間の依存関係

プロジェクトの各ディレクトリ・モジュールは、責務ごとに明確に分離されており、以下のような依存関係を持っています。

```mermaid
graph TD
    classDef main fill:#ffbfbf,stroke:#333,stroke-width:1px,color:#000
    classDef pipeline fill:#fff0bf,stroke:#333,stroke-width:1px,color:#000
    classDef stages fill:#bfffbf,stroke:#333,stroke-width:1px,color:#000
    classDef model fill:#dfbfff,stroke:#333,stroke-width:1px,color:#000

    Main[src/main.py]:::main --> Pipeline[src/pipeline/]:::pipeline
    Pipeline --> Stages[src/stages/]:::stages
    Stages --> Model[src/model/]:::model
```

1.  **`src/main.py` (CLI / Entrypoint)**
    - **役割**: ユーザーからのコマンド入力(`gen-script`, `gen-subtitle`等)を受け取り、適切なパイプラインを実行します。
    - **依存**: `src/pipeline/` (実行フローの呼び出し)
2.  **`src/pipeline/` (Orchestration)**
    - **役割**: 複数の処理(Stage)をつなぎ合わせ、I/Oを含めた一連の作業フローを定義します。
    - **依存**: `src/stages/` (アトミックな処理), `src/util/` (ファイル保存等)
3.  **`src/stages/` (Processing Functions)**
    - **役割**: Gemini APIによるテキスト生成や、MoviePyを用いた動画編集などのアトミックな機能を提供します。
    - **依存**: `src/model/` (型定義), `src/util/` (APIクライアント等)
    - **外部依存**: `moviepy`, `pydub`
4.  **`src/util/` (Utilities)**
    - **役割**: プロジェクト全体で使い回す汎用的な処理（APIクライアント初期化、ロギング、JSONの読み書き）をまとめます。
    - **外部依存**: `google-genai` (Gemini API呼び出し), `python-dotenv` (環境変数展開)
5.  **`src/model/` (Data Models)**
    - **役割**: APIの構造化出力や内部でやり取りするデータのスキーマを定義します。
    - **外部依存**: `pydantic`
