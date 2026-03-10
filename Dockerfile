# ベースイメージとして軽量なPython 3.12-slimを使用
FROM python:3.12-slim

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係ファイルのコピーとインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードのコピー
COPY src/ .

# アプリケーションの実行（デフォルトで main.py を実行）
CMD ["python", "main.py"]
