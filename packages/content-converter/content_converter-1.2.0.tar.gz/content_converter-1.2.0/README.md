# Content-Converter

テキストファイルを指定されたプロンプトとテンプレートに基づいて変換するツールです。

## 概要

Content-Converterは、LLMを活用して、入力テキストを指定されたプロンプトとテンプレートに基づいて変換します。CI/CDパイプラインから呼び出せる形式で提供され、自動化された変換処理を可能にします。

## 主な機能

- テキストファイルの変換処理
- プロンプトベースの変換制御
- テンプレートベースの出力形式定義
- 複数LLMプロバイダー対応
- カスタムプロンプト機能
- 任意のテキスト形式に対応

## ドキュメント

- [インストールガイド](docs/installation.md)
- [機能詳細](docs/features.md)
- [アーキテクチャー設計書](docs/architecture.md)
- [仕様書](docs/specification.md)
- [サポートされているLLMプロバイダー](docs/supported_llm_providers.md)

## サポートされているLLMプロバイダー

サポートされているLLMプロバイダーとその設定方法については、[LLMプロバイダー一覧](docs/supported_llm_providers.md)を参照してください。

## 使用方法

`content-converter` を使用する前に、Pythonの仮想環境を適切にセットアップし、依存関係が完全にインストールされていることを確認してください。

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

```bash
content-converter --input article.md --template template.md --output converted.md
```

詳細な使用方法や設定については、[仕様書](docs/specification.md)を参照してください。

## 出力形式

- 任意のテキスト形式に対応
- テンプレートベースの出力形式定義
- 入力と同形式の出力をサポート
- 環境変数またはコマンドライン引数でのAPIキー指定（[詳細](docs/specification.md#apiキーの指定方法)）

## 依存関係

必須依存パッケージ:
- pyyaml>=6.0
- python-frontmatter>=1.0.0
- requests>=2.28.0
- python-dotenv>=1.0.0
- markdown>=3.4.0
- pydantic>=2.5.2

## ライセンス

MIT License