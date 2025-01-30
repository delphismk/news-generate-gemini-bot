# ニュース創作ボット（News Generate Gemini Bot）
その日のニュースをタイトルと概要を元にAIに記事内容を創作してもらい、自分のメールにPDF形式でその記事内容を送ってもらうpythonスクリプトです

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

##使い方
1. apikey.envを作成しNEWSAPIのAPIキーとGEMINI　APIのAPIキーをセット(無料)
2. apikey.envにGmailのアドレスとアプリパスワードをセット
3. news-guess-gemini.py をダウンロードし、ローカル環境で実行

## 今後の課題
・このスクリプトをGCP上でスケジューラ実行できるようにする
・スクレイピング可のニュースサイト(候補：The Gurdian)を調査し、記事本文をスクレイピングしGEMINIに要約してもらう処理へ変更することで記事内容の信憑性・クオリティを上げる

## 背景

### 本スクリプトの作成背景
私はテレビを持っておらず政治・経済・技術情報をyoutubeで得ることが多かったため、特定分野のニュースには詳しくなるが幅広くはニュースを知れていないという状況が続いていた。しかしわざわざ手を動かしてニュースアプリやブラウザを見に行くという作業を毎日行うのは少し面倒になりそうだと感じたので効率的に幅広くその日のニュースを取得できる方法はないかと考えていた。
そこで思いついたのがwebスクレイピング。GoogleニュースやYahoo!ニュースから記事を抜きとりAIに要約させて毎日9時に自分のメールやLINEに要約結果を送って貰えば、要約結果はドキュメント形式であるかつ手を動かす必要もないので短時間で効率よく幅広い情報を取得できると考えていた.しかし大抵のwebサイトやアプリがスクレイピングを禁止していたことを後から知り、API利用であれば記事のタイトルと概要だけは取得できることが判明したので、今回はこのようなスクリプト作成に至った。


### 本スクリプト作成の手段と私のスキルセット
私はプログラミングスキルが乏しく0からこのようなスクリプトを書けないため、Chatgpt-4oの助けを借りながら完成させたスクリプトとなります。ご承知おきください。(Udemyでpythonの勉強中




