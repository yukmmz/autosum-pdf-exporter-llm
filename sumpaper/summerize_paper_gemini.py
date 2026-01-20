import os
from pathlib import Path
import time
import pdfkit
import markdown
from dotenv import load_dotenv

from google import genai
from google.genai import types

__all__ = [
    'summarize_pdf_gemini', 
    'list_available_models',
    ]

# APIキーを環境変数から取得、または直接文字列で指定
load_dotenv()

# # 修正後: Pathを使って .env の場所を絶対パスで指定する
# current_file_path = Path(__file__).resolve()
# # このファイルが sumpaper/ にあると仮定し、親の親(ルート)の .env を探す
# # 構成に合わせて .parent の数を調整してください。
# # sumpaper/summerize_paper_gemini.py なら .parent で sumpaper、もう一つ .parent でルート
# env_path = current_file_path.parent.parent / '.env'
# if not env_path.exists():
#     raise ValueError(f".env file not found at expected location: {env_path}")

# load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in environment variables. please set it in .env file or your environment.")
client = genai.Client(api_key=api_key)

PATH_WKHTMLTOPDF = os.getenv("WKHTMLTOPDF_PATH")
if not PATH_WKHTMLTOPDF:
    raise ValueError("WKHTMLTOPDF_PATH is not set in environment variables. please set it in .env file or your environment.")

# PATH_WKHTMLTOPDF が正しいかチェック
if not Path(PATH_WKHTMLTOPDF).exists():
    raise ValueError(f"WKHTMLTOPDF_PATH '{PATH_WKHTMLTOPDF}' does not exist. Please check the path.")

print("Found GOOGLE_API_KEY and WKHTMLTOPDF_PATH.")

def list_available_models(required_actions=['generateContent', 'batchGenerateContent']):
    print("利用可能なモデル一覧:")
    
    # client.models.list() を使用します
    for m in client.models.list():
        # required_actions がすべて supported_generation_methods に含まれているかチェック
        if all(method in m.supported_actions  for method in required_actions):
            print(f"name: {m.name}")
            print(f"description: {m.description}")
            print(f"supported_actions: {m.supported_actions}")
            print("-" * 30)
    

def summarize_pdf_gemini(
    pdf_path, 
    prompt_text, 
    output_pdf_path, 
    model_name=None,
    verbose=False,
    show_md=False,
    font_size=30,
    ):
    

    # --- model_nameの自動選択 ---
    if model_name is None:
        # ['generateContent', 'batchGenerateContent'] の両方に対応したモデルを一つ選ぶ。
        # もし無ければ、'generateContent' に対応したモデルを選ぶ。
        available_models = []
        for m in client.models.list():
            if all(action in m.supported_actions for action in ['generateContent', 'batchGenerateContent']):
                available_models.append(m.name)
                break # 最初に見つけたモデルを使う
        if available_models:
            model_name = available_models[0]
        else:
            for m in client.models.list():
                if 'generateContent' in m.supported_actions:
                    available_models.append(m.name)
                    break # 最初に見つけたモデルを使う
            if available_models:
                model_name = available_models[0]
            else:
                raise ValueError("No suitable model found that supports 'generateContent' action.")
    if verbose:
        print(f"Using model: {model_name}")
    
    
    # 2. PDFファイルのアップロード
    if verbose:
        print(f"Uploading {pdf_path}...")
    file_upload = client.files.upload(file=pdf_path)

    # 3. 処理完了待ち
    if verbose:
        print(f"Processing file: {file_upload.name}")
    while file_upload.state.name == "PROCESSING":
        if verbose: print(".", end="", flush=True)
        time.sleep(2)
        file_upload = client.files.get(name=file_upload.name)

    if file_upload.state.name == "FAILED":
        raise ValueError("File processing failed.")
    
    if verbose: print("\nFile processing complete.")
    time.sleep(5)  # 安全のため少し待つ


    # 4. コンテンツ生成
    if verbose: print("Generating summary...")
    
    # モデル名を 'gemini-2.5-flash' に変更 (これで429エラーを回避)
    # configでシステムプロンプトや温度パラメータも設定可能
    response = client.models.generate_content(
        model=model_name,
        contents=[
            types.Content(
                parts=[
                    types.Part.from_uri(
                        file_uri=file_upload.uri,
                        mime_type=file_upload.mime_type),
                    types.Part.from_text(text=prompt_text)
                ]
            )
        ]
    )
    markdown_text = response.text
    if verbose: print("Summary generated.")

    if show_md:
        print("-" * 30)
        print(markdown_text)
        print("-" * 30)

    # --- 後半：markdown-pdfによるPDF化 ---
    if verbose: print(f"Exporting to {Path(output_pdf_path).absolute()}...")
    
    md2pdf_pdfkit(markdown_text, output_pdf_path, font_size=font_size)
    
    return


def md2pdf_pdfkit(markdown_text, output_path, font_size=30):
    # HTMLへ変換
    html_body = markdown.markdown(markdown_text)
    
    # 日本語フォントを明示的に指定したHTML全体を構築
    full_html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: "MS Mincho", "Hiragino Mincho ProN", serif; font-size: {font_size}pt; }}
        </style>
    </head>
    <body>{html_body}</body>
    </html>
    """
    
    # PDF保存 (wkhtmltopdfのインストールが必要です)
    config = pdfkit.configuration(wkhtmltopdf=PATH_WKHTMLTOPDF)
    # pdfkit.from_string(full_html, output_path)
    pdfkit.from_string(full_html, output_path, configuration=config)


def test():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # 対象のPDFファイルパス
    pdf_file_path = "../data/paper.pdf" 
    prompt_path = "../data/prompt_sample.md"
    output_pdf_path = Path(pdf_file_path).parent / "summary_output.pdf"

    # get prompt from file
    with open(prompt_path, 'r', encoding='utf-8') as f:
        my_prompt = f.read()

    try:
        # summary = summarize_pdf(pdf_file_path, my_prompt, model_name='gemini-2.5-pro')
        summary = summarize_pdf_gemini(pdf_file_path, my_prompt, output_pdf_path=output_pdf_path, show_md=True)
    except Exception as e:
        print(f"Error: {e}")


def test_md2pdf_pdfkit():
    # filepath = "../data/markdown_text.md"
    filepath = "../BU/md_sample.md"
    with open(filepath, 'r', encoding='utf-8') as f:
        markdown_text = f.read()
    output_pdf_path = Path(filepath).parent / "markdown_output.pdf"
    md2pdf_pdfkit(markdown_text, output_pdf_path, font_size=30)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # list_available_models(required_actions=['generateContent', 'batchGenerateContent'])

    # test()
    # test_markdown_pdf()
    test_md2pdf_pdfkit()