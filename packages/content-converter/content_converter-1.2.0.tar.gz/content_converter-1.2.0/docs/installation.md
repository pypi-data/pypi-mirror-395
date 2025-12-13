# Content-Converter インストールガイド

## 環境要件

- Python 3.8 以上
- pip（Python パッケージマネージャー）
- Git（オプション：ソースからのインストール時）

## インストール方法

### 仮想環境の利用を推奨

```bash
python3 -m venv venv
source venv/bin/activate
```

### 1. PyPI からのインストール（推奨）

```bash
pip install content-converter
```

**重要: 仮想環境でのインストールに関する注意点**
`pip install content-converter` を実行した際に、稀に依存関係のインストールが不完全となる場合があります。特に `google.generativeai` モジュールが見つからない (`ModuleNotFoundError`) などのエラーが発生した場合は、以下の手順で対処してください。

1.  仮想環境内で `pip` を最新の状態に更新します。
    ```bash
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip
    ```
2.  その後、`google-generativeai` を明示的にインストールします。
    ```bash
    pip install google-generativeai
    ```
これらの手順は、依存関係の完全な解決に役立ちます。

### 2. ソースからのインストール

（仮想環境を有効化した状態で実行してください）

```bash
# リポジトリのクローン
git clone https://github.com/centervil/Content-Converter.git
cd Content-Converter

# 仮想環境の作成・有効化（未実施の場合）
python3 -m venv venv
source venv/bin/activate

# 依存関係のインストール
pip install -e ".[dev]"
```

## 依存関係

### 必須パッケージ

- pyyaml>=6.0
- python-frontmatter>=1.0.0
- requests>=2.28.0
- python-dotenv>=1.0.0
- markdown>=3.4.0
- pydantic>=2.5.2

### 開発用パッケージ（オプション）

- pytest>=7.0.0
- pytest-cov>=4.0.0
- black>=23.0.0
- flake8>=6.0.0
- mypy>=1.0.0

## 設定

### 1. API キーの設定

#### 環境変数を使用する場合

```bash
# Google Geminiを使用する場合
export GOOGLE_API_KEY='your-api-key'

# OpenRouterを使用する場合
export OPENROUTER_API_KEY='your-api-key'
```

#### コマンドライン引数で指定する場合

```bash
# Google Geminiを使用する場合
--api-key gemini:your-api-key

# OpenRouterを使用する場合
--api-key openrouter:your-api-key
```

### 2. 設定ファイル（オプション）

`~/.content-converter/config.yaml`に設定ファイルを作成できます：

```yaml
default_llm_provider: gemini
default_model: gemini-pro
api_keys:
  gemini: your-api-key
  openrouter: your-api-key
```

## 動作確認

インストール後、以下のコマンドで動作確認ができます：

```bash
content-converter --version
```

## トラブルシューティング

### 1. 依存関係のエラー

```bash
# 依存関係の再インストール
pip install --upgrade -r requirements.txt
```

### 2. API キーの問題

- 環境変数が正しく設定されているか確認
- API キーが有効か確認
- コマンドライン引数と環境変数の優先順位を確認

### 3. パーミッションの問題

```bash
# 実行権限の付与
chmod +x /path/to/content-converter
```

## アンインストール

```bash
pip uninstall content-converter
```

## サポート

問題が発生した場合は、以下の方法でサポートを受けることができます：

1. GitHub Issues での報告
2. ドキュメントの確認
3. コミュニティフォーラムでの質問
