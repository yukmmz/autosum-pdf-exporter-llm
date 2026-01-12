
# SumPaper

簡単な論文要約自動化ツールです。指定したフォルダ内のPDFをGoogle Gemini（GenAI）で要約し、MarkdownからPDFを生成します。  
指定したフォルダ内の各pdfファイルに対して、指定したプロンプトを用いて要約を行い、結果をPDFとして保存します。  
（pdf アップロード → プロンプト入力 → 要約生成 → PDF出力）x （pdf 数） の処理を自動化します。  

**動作確認環境**
- Python 3.12.10

## 前提
- `wkhtmltopdf` がシステムにインストールされていること（HTML→PDF変換に使用）
- Google Gemini APIキー（`GOOGLE_API_KEY`）を取得していること

## セットアップ手順

1. 依存パッケージをインストール  
    ```bash
    pip install -r requirements.txt
    ```

1. `wkhtmltopdf` をインストール
   - ダウンロードページ: https://wkhtmltopdf.org/downloads.html

1. 環境変数ファイルを作成
   - ` .env.example` をコピーして `.env` を作成し、次を設定してください:
      ```
      GOOGLE_API_KEY="<あなたのAPIキー>"
      WKHTMLTOPDF_PATH=<wkhtmltopdfの実行ファイルパス>
      ```

## 使い方（例）

- 利用可能なモデルの一覧を表示:
    ```powershell
    python main.py --list-models
    ```

- フォルダ内のPDFを順次要約して出力:
    ```powershell
    python main.py -i ./data -o ./data/output -p ./data/prompt_sample.md
    ```

主なオプション:
- `--input-dir, -i` : 入力PDFが置かれたフォルダ（デフォルト `./data`）
- `--output-dir, -o`: 出力先フォルダ（未指定なら `<input_dir>/output`）
- `--prompt-path, -p`: 要約に使うプロンプトのMarkdownファイル（デフォルト `./data/prompt_sample.md`）
- `--model-name, -m`: 使用するモデル名（指定しないと自動選択）

## 注意事項 / トラブルシューティング
- `.env` に `GOOGLE_API_KEY` が未設定だと起動時にエラーになります。
- `WKHTMLTOPDF_PATH` は実行環境の実際のパスに合わせてください。
- Windowsで実行する場合、`wkhtmltopdf` のパスにスペースが含まれるときは `.env` に設定する際に正しく記述してください。


