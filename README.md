

TODO
- 複数pdfを扱うループを作る
  - 指定されたフォルダの全てのpdfのパスを、以下のようなリストに入れる
    state_arr = [[pdf_path1, False], [pdf_path2, False], ...] # Falseは未処理を意味する
  - 以下のループを max_loop 回まで繰り返す
    - 未処理リストの論文pdfから論文要約pdfを作成する。（output のPDFの名前を、元のPDF名＋"_summary.pdf" にする）
    - 作成できたら、state_arr[i][1] = Trueにして、次の論文へ進む。
    - エラーが出たら少し待って次の論文へ進む。
    - 未処理リストの末尾まできたときに、終わっていない論文があれば、次のループに進み、再度処理を試みる。
    - 全ての論文が処理できていたらbreakする。


install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html
