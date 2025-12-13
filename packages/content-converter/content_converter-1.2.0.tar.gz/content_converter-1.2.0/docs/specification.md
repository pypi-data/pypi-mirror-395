# Content-Converter 仕様書

## 概要

Content-Converter は、テキストファイルを指定されたプロンプトとテンプレートに基づいて変換するツールです。LLMを活用して、入力テキストを変換し、指定されたテンプレートに従って出力を生成します。CI/CD パイプラインから呼び出せる形式で提供され、自動化された変換処理を可能にします。

**重要: インストールに関する注意点**
パッケージのインストール時に、稀に依存関係の解決に問題が発生する場合があります。特に`google.generativeai`モジュールが見つからない等のエラーが発生した場合は、[インストールガイド](installation.md)のトラブルシューティングセクションを参照してください。

## ユースケース

### テキスト変換の自動化

**目的**: 入力テキストを指定されたプロンプトとテンプレートに基づいて変換

**フロー**:

1. 入力ファイル、テンプレートファイル、プロンプトファイルを指定
2. `content-converter`を実行
3. 変換されたテキストを出力

## インターフェース

### コマンドライン引数

| 引数             | 説明                             | 必須 | デフォルト値             |
| ---------------- | -------------------------------- | :--: | ------------------------ |
| `--input`        | 入力ファイルのパス               |  ✓   | -                        |
| `--template`     | テンプレートファイルのパス       |  ✓   | -                        |
| `--prompt`       | カスタムプロンプトファイルのパス |      | デフォルトプロンプト     |
| `--output`       | 出力先ファイルパス               |      | 標準出力                 |
| `--llm-provider` | 使用する LLM プロバイダー        |      | openai                   |
| `--model`        | 使用する LLM モデル              |      | プロバイダーのデフォルト |

## API キーの指定方法

### 環境変数を使用する場合

```bash
export GOOGLE_API_KEY='your-api-key'  # Google Geminiを使用する場合
export OPENROUTER_API_KEY='your-api-key'  # OpenRouterを使用する場合
```

### コマンドライン引数で指定する場合

```bash
# Google Geminiを使用する場合
--api-key gemini:your-api-key

# OpenRouterを使用する場合
--api-key openrouter:your-api-key
```

> **注意**: コマンドライン引数で指定された API キーは、環境変数よりも優先されます。

### 入力ファイル

変換元となるテキストファイル。任意の形式が使用可能です。

### テンプレートファイル

出力形式を定義するファイル。任意の形式が使用可能です。

### プロンプトファイル

LLM への指示を含むテキストファイル。デフォルトプロンプトを使用するか、カスタムプロンプトを指定できます。

例:

```text
以下の入力テキストを指定されたテンプレートの形式に変換してください。

# 入力テキスト
{{input}}

# 使用するテンプレート
{{template}}

# 出力要件
- テンプレート内のプレースホルダーを適切に置き換えてください
- フォーマットを維持してください
- 構造を保持してください
```

## 使用例

### 基本的な使用方法

```bash
content-converter --input article.md --template template.md --output converted.md
```

### カスタムプロンプトの使用

```bash
content-converter --input article.md --template template.md --prompt custom_prompt.txt --output converted.md
```

### 異なる LLM プロバイダーの指定

```bash
content-converter --input article.md --template template.md --llm-provider gemini --model gemini-pro --output converted.md
```

## 出力形式

このツールは、指定されたテンプレートに基づいて任意の形式のテキストを出力できます。

- テンプレートの形式に制限はありません
- 入力と同様、任意のテキスト形式に対応
- 出力は指定されたテンプレートの構造に従います
