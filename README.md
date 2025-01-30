# ニュース生成ボット（News Generate Gemini Bot）
NewsAPI からタイトル(title)と概要(description)を取得し、Geminiに取得したタイトルと概要から記事を創作してもらい、 PDF に変換し、メールで送信する Python スクリプトです。

##  機能
1. NewsAPI からタイトル(title)と概要(description)を取得
2. タイトルと概要を元に記事内容を創作するプロンプトをGeminiに投げる
3. Geminiが創作した記事を PDF に変換
4. プログラム実行時にenvファイルに定義したGmailアドレスにPDFが送信される

## 🛠 セットアップ
1. 必要な Python パッケージをインストール
   ```sh
   pip install -r requirements.txt
