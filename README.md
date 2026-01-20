
# autosum-pdf-exporter-llm

簡単なpdf要約自動化ツールです。指定したフォルダ内のPDFをGoogle Gemini（GenAI）で要約し、MarkdownからPDFを生成します。  
指定したフォルダ内の各pdfファイルに対して、指定したプロンプトを用いて要約を行い、結果をPDFとして保存します。  
（pdf アップロード → プロンプト入力 → 要約生成 → PDF出力）x （pdf 数） の処理を自動化します。  

**動作確認環境**
- Python 3.12.10


## セットアップ手順

1. 依存パッケージをインストール  
    ```bash
    pip install -r requirements.txt
    ```

1. `wkhtmltopdf` をインストール  
    ダウンロードページ: https://wkhtmltopdf.org/downloads.html

1. Google の API キーを取得
   1. [Google AI Studio](https://aistudio.google.com/) にアクセスし、Googleアカウントでログイン
   2. "Get API Key" から API キーを取得

1. 環境変数ファイルを作成  
    ` .env.example` をコピーして `.env` を作成し、次を設定してください:
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
    python main.py -i ./data -o ./data/output -p ./data/prompt_sample.md -n 5 -f 30
    ```

主なオプション:
- `--input-dir, -i` : 入力PDFが置かれたフォルダ（デフォルト `./data`）
- `--output-dir, -o`: 出力先フォルダ（未指定なら `<input_dir>/output`）
- `--prompt-path, -p`: 要約に使うプロンプトのMarkdownファイル（デフォルト `./data/prompt_sample.md`）
- `--model-name, -m`: 使用するモデル名（指定しないと自動選択）
- `--max-loop, -n`: 要約の最大繰り返し回数（デフォルト 5）
- `--font-size, -f`: PDF出力時のフォントサイズ。スマホで読むなら30ほどがおすすめ。PCで読むなら14ほどがおすすめ （デフォルト 30）

## 注意事項 / トラブルシューティング
- `.env` に `GOOGLE_API_KEY` が未設定だと起動時にエラーになります。
- `WKHTMLTOPDF_PATH` は実行環境の実際のパスに合わせてください。
- 'The model is overloaded. Please try again later.' というエラーが良く出るので、`--max-loop` をある程度大きくして繰り返しトライさせるか、時間を空けて再度実行してください（ただ、リクエスト数が多いとAPIキーの制限に引っかかる可能性があります）。


## to be improved
<!-- - フォントをスマホで見やすいサイズにする -->
<!-- - 冗長な出力をさせないようにする -->
- プロンプトをマシにする
  - pro の出力の手本をのせる
  - 最低限 pro で所望の返答が来る必要。
  - 目的を伝える
