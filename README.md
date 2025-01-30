# ニュース創作ボット（News Generate Gemini Bot）
タイトルと概要を元にニュースの記事内容をAIに創作してもらい、自分のメールにPDF形式でその記事内容を送ってもらうpythonスクリプト

##  機能
1. NewsAPI からタイトル(title)と概要(description)を取得
2. タイトルと概要を元に記事内容を創作するプロンプトをGeminiに投げる
3. Geminiが創作した記事を PDF に変換
4. プログラム実行時にenvファイルに定義したGmailアドレスにPDFが送信される

## ライブラリ
- import os
- import sys
- import time
- import google.generativeai as genai
- import requests
- import smtplib
- from email.message import EmailMessage
- from dotenv import load_dotenv
- from weasyprint import HTML

## .envファイルについて
- NEWSAPI_KEY=your_newsapi_key
- GEMINI_API_KEY=your_gemini_api_key
- GMAIL_USER=your_email
- GMAIL_PASS=your_email_password
- GMAIL_RECEIVER=receiver_email

## 使い方
1. apikey.envを作成しNEWSAPIのAPIキーとGEMINI　APIのAPIキーをセット(無料)
2. apikey.envにGmailのアドレスとアプリパスワードをセット
3. news-guess-gemini.py をダウンロードし、ローカル環境で実行

## 今後の課題
・このスクリプトをGCP上でスケジューラ実行できるようにする
・スクレイピング可のニュースサイト(候補：The Gurdian)を調査し、記事本文をスクレイピングしGEMINIに要約してもらう処理へ変更することで記事内容の信憑性・クオリティを上げる

## 背景

### 本スクリプトの作成背景
私はテレビを持っておらず、YouTubeでニュースを得ることが多かったため、特定分野には詳しくなるものの、幅広いニュースを知る機会が少なかった。
しかし、毎日ニュースアプリを開くのは面倒だと感じたため、効率的に情報収集できる方法を考えた。
最初は Web スクレイピングでニュース記事を取得しようとしたが、スクレイピングを禁止しているサイトが多いことを知り、代わりに NewsAPI を使って記事タイトルと概要を取得する方法を選択。
そこから Gemini を使って創作記事を生成し、PDF にまとめてメールで送信するスクリプトを作成するに至った。


### 本スクリプト作成の手段と私のスキルセット
現在、Pythonは学習中であり、本スクリプトはChatGPT-4oの助けを借りながら試行錯誤して作成しました。(100回以上やり取りしました)
Udemyを活用してPythonを学習中であり、今後さらにスクリプトの精度を高め、GCPなどを活用したクラウド環境への展開も試みていきます。




