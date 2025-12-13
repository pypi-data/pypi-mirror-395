# Content-Converter 機能詳細

## コア機能

### 1. プロンプト生成

#### 概要

入力ファイル、テンプレートファイル、プロンプトファイルから、LLM に渡すプロンプトを生成します。

#### 主な機能

- 入力ファイルの読み込み
- テンプレートファイルの読み込み
- プロンプトファイルの読み込み
- プロンプトの生成と検証

#### 使用例

```bash
content-converter --input article.md --template template.md --prompt custom_prompt.txt
```

### 2. LLM によるテキスト変換

#### 概要

生成されたプロンプトに基づいて、LLM を使用してテキストを変換します。

#### 主な機能

- LLM プロバイダーとの通信
- プロンプトの送信
- レスポンスの処理
- エラーハンドリング

#### 使用例

```bash
content-converter --input article.md --template template.md --llm-provider gemini --model gemini-pro
```

### 3. ファイル出力

#### 概要

LLM によって変換されたテキストをファイルとして出力します。

#### 主な機能

- 出力ファイルの生成
- エンコーディングの処理
- エラーハンドリング
- 出力形式の検証

#### 使用例

```bash
content-converter --input article.md --template template.md --output converted.md --encoding utf-8
```

## 設定オプション

### 1. LLM プロバイダー設定

#### 対応プロバイダー

- Google Gemini
- OpenRouter

#### 設定方法

```bash
# 環境変数
export GOOGLE_API_KEY='your-api-key'
export OPENROUTER_API_KEY='your-api-key'

# コマンドライン引数
--llm-provider gemini --model gemini-pro
```

### 2. 出力設定

#### オプション

- 出力ファイル名
- 出力ディレクトリ
- 出力形式
- エンコーディング

#### 使用例

```bash
content-converter --input article.md --template template.md --output converted.md --encoding utf-8
```

### 3. デバッグ設定

#### オプション

- ログレベル
- 詳細なエラー情報
- デバッグモード
- プログレス表示

#### 使用例

```bash
content-converter --input article.md --template template.md --debug --log-level DEBUG
```

## エラーハンドリング

### 1. 入力エラー

- ファイルが見つからない
- ファイル形式が不正
- テンプレートが不正
- プロンプトが不正

### 2. LLM エラー

- API キーが無効
- レート制限
- タイムアウト
- レスポンスエラー

### 3. 出力エラー

- 出力先が書き込み不可
- ディスク容量不足
- エンコーディングエラー
- パーミッションエラー
