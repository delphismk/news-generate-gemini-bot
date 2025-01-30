# ニュース生成ボット（News Generate Gemini Bot）

NewsAPI からニュースタイトルを取得し、Gemini で記事を生成して PDF に変換し、メールで送信する Python スクリプトです。

## 🚀 機能
- NewsAPI からニュース取得
- Gemini で記事生成
- 生成した記事を PDF に変換
- Gmail で毎朝 9 時に自動送信

## 🛠 セットアップ
1. 必要な Python パッケージをインストール
   ```sh
   pip install -r requirements.txt
