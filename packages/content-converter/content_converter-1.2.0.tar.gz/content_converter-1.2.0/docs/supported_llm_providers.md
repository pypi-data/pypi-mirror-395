# サポートされているLLMプロバイダー

Content-Converterでは、以下のLLMプロバイダーをサポートしています。APIキーは環境変数またはコマンドライン引数で指定できます。

### APIキーの指定方法

1. **環境変数を使用する場合**
   - 各プロバイダーに対応する環境変数にAPIキーを設定
   - 例: `export GOOGLE_API_KEY='your-api-key'`

2. **コマンドライン引数で指定する場合**
   - `--api-key` オプションで直接指定
   - 例: `--api-key gemini:your-api-key` または `--api-key openrouter:your-api-key`

> **注意**: コマンドライン引数で指定されたAPIキーは、環境変数よりも優先されます。

## Google Gemini

- **プロバイダー名**: `gemini`
- **認証方法**: 
  - 環境変数: `GOOGLE_API_KEY`
  - コマンドライン引数: `--api-key gemini:YOUR_API_KEY`
- **詳細**: [公式ドキュメント](https://ai.google.dev/)を参照

## OpenRouter

- **プロバイダー名**: `openrouter`
- **認証方法**: 
  - 環境変数: `OPENROUTER_API_KEY`
  - コマンドライン引数: `--api-key openrouter:YOUR_API_KEY`
- **詳細**: [公式ドキュメント](https://openrouter.ai/docs)を参照

## デフォルト設定

- **デフォルトプロバイダー**: `gemini`
- **デフォルトモデル**: `gemini-2.0-flash-001`

各プロバイダーで利用可能なモデルの詳細は、各プロバイダーの公式ドキュメントを参照してください。
