# ニュース創作ボット（News Generate Gemini Bot）
記事のタイトルと概要を元にニュースの記事の要約をAIに作成してもらい、自分のメールにPDF形式でニュースを送ってもらうpythonスクリプト

---

## **🔹 機能**
1. **NewsAPI** から最新ニュースのタイトル・概要・本文を取得
2. 取得した情報をもとに **Gemini API** にニュース記事の要約を生成させる
3. **生成された要約を PDF に変換**
4. **Gmail を利用して PDF を指定のメールアドレスへ送信**

---

## **📌 使用ライブラリ**
- `os`
- `sys`
- `google.generativeai`
- `requests`
- `smtplib`
- `email.message.EmailMessage`
- `dotenv.load_dotenv`
- `weasyprint.HTML`

---

## **🛠 環境変数 (`.env` ファイル)**
本スクリプトの実行には `.env` ファイルが必要です。  
ルートディレクトリに `.env` を作成し、以下のように設定してください。

```plaintext
NEWSAPI_KEY=your_newsapi_key
GEMINI_API_KEY=your_gemini_api_key
GMAIL_USER=your_email
GMAIL_PASS=your_email_password
GMAIL_RECEIVER=receiver_email
```
---

## カスタマイズ
### 取得する記事数
main()内のmaxarticlesで指定してください<br>
(デフォルト：maxarticles=5)
### 取得したいニュースジャンル
get_latest_news(max_articles)内のurlのクエリパラメタを変更してください<br>
(デフォルト：country=us,category=business)<br>
※[NewsAPIの詳細なIF定義](https://newsapi.org/docs/endpoints/top-headlines)

---
## 注意点
### 記事の信頼性
NewsAPIのDEVプランでは取得できる記事本文に限りがある(200字以降は切り捨てられる)こと、記事本文が存在しない記事もあること。これらからGEMINIに十分な情報をINPUTできていない可能性がある。


