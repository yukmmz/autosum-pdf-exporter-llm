import os
import time
from pathlib import Path
import sumpaper as sp
import argparse



def test():
    
    sp.list_available_models()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # 対象のPDFファイルパス
    pdf_path = "./data/paper.pdf" 
    prompt_path = "./data/prompt_sample.md"
    output_pdf_path = Path(pdf_path).parent / "summary_output.pdf"

    # get prompt from file
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_text = f.read()

    try:
        # summary = summarize_pdf(pdf_file_path, my_prompt, model_name='gemini-2.5-pro')
        sp.summarize_pdf_gemini(
        pdf_path, 
        prompt_text, 
        output_pdf_path, 
        model_name=None,
        show_md=False,
        )
    except Exception as e:
        print(f"Error: {e}")



def arg_parser():
    parser = argparse.ArgumentParser(description='Summarize PDFs in a folder')
    parser.add_argument('--input-dir', '-i', default='./data/input', help='Input directory containing PDFs')
    parser.add_argument('--output-dir', '-o', default=None, help='Output directory for summaries (defaults to <input_dir>/output)')
    parser.add_argument('--prompt-path', '-p', default='./data/prompt_sample.md', help='Path to prompt file')
    parser.add_argument('--model-name', '-m', default='gemini-2.5-flash', help='Model name')
    parser.add_argument('--max-loop', '-n', type=int, default=3, help='Max loop count')
    return parser.parse_args()


def _main():
    """- 複数pdfを扱うループを作る
  - 指定されたフォルダの全てのpdfのパスを、以下のようなリストに入れる
    state_arr = [[pdf_path1, False], [pdf_path2, False], ...] # Falseは未処理を意味する
  - 以下のループを max_loop 回まで繰り返す
    - 未処理リストの論文pdfから論文要約pdfを作成する。（output のPDFの名前を、元のPDF名＋"_summary.pdf" にする）
    - 作成できたら、state_arr[i][1] = Trueにして、次の論文へ進む。
    - エラーが出たら少し待って次の論文へ進む。
    - 未処理リストの末尾まできたときに、終わっていない論文があれば、次のループに進み、再度処理を試みる。
    - 全ての論文が処理できていたらbreakする。
    """
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    args = arg_parser()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir) if args.output_dir else (input_dir / "output")
    prompt_path = args.prompt_path
    model_name = args.model_name
    max_loop = args.max_loop


    debug = False

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # get prompt from file
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_text = f.read()

    pdf_list = [f for f in input_dir.glob("*.pdf")]
    state_arr = [[pdf_path, False] for pdf_path in pdf_list]
    for loop_idx in range(max_loop):
        print(f"=== Loop {loop_idx+1} ===")
        # あといくつ残っているか表示
        remaining = sum(1 for _, done in state_arr if not done)
        print(f"Papers remaining: {remaining}")

        all_done = True
        for i, (pdf_path, done) in enumerate(state_arr):
            if done:
                continue
            print(f"--- Processing {pdf_path.name} ---")
            output_pdf_path = output_dir / f"{pdf_path.stem}_summary.pdf"
           
            if debug:
                sp.summarize_pdf_gemini(
                    pdf_path, 
                    prompt_text, 
                    output_pdf_path, 
                    model_name=model_name,
                    show_md=False,
                    verbose=True,
                )
                state_arr[i][1] = True  # Mark as done
                print(f"Processed {pdf_path.name} successfully.")
            else:
                try:
                    sp.summarize_pdf_gemini(
                        pdf_path, 
                        prompt_text, 
                        output_pdf_path, 
                        model_name=model_name,
                        show_md=False,
                        verbose=False,
                    )
                    state_arr[i][1] = True  # Mark as done
                    print(f"Processed {pdf_path.name} successfully.")
                except Exception as e:
                    print(f"Error processing {pdf_path.name}: {e}")
                    all_done = False
            
            time.sleep(5)  # 少し待つ
        if all_done:
            print("All papers processed successfully.")
            break
    



if __name__ == "__main__":
    _main()