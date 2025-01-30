import os
import sys
import time
import google.generativeai as genai
import requests
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from weasyprint import HTML

# PyCharm の print バッファリングを回避（リアルタイム表示）
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

# .env ファイルを読み込む
load_dotenv("apikey.env")

# APIキーの取得
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
GMAIL_RECEIVER = os.getenv("GMAIL_RECEIVER")

# APIキーの確認
if not NEWSAPI_KEY or not GEMINI_API_KEY:
    print("❌ APIキーが見つかりません。'apikey.env' を確認してください。")
    exit(1)

if not GMAIL_USER or not GMAIL_PASS or not GMAIL_RECEIVER:
    print("❌ Gmailの設定が不足しています。'apikey.env' を確認してください。")
    exit(1)

# Gemini APIのセットアップ
genai.configure(api_key=GEMINI_API_KEY)

# NewsAPIのエンドポイント
NEWSAPI_URL = f"https://newsapi.org/v2/top-headlines?country=us&category=general&apiKey={NEWSAPI_KEY}"

def get_latest_news():
    """NewsAPI からタイトルと概要を取得"""
    try:
        print(f"🛠️ NewsAPI へリクエスト送信中: {NEWSAPI_URL}")
        response = requests.get(NEWSAPI_URL, timeout=10)  # タイムアウトを設定
        data = response.json()

        if data.get("status") != "ok":
            print(f"⚠️ NewsAPI エラー: {data.get('message')}")
            return []

        articles = data.get("articles", [])
        if not articles:
            print("⚠️ 取得した記事が空でした。")
            return []

        print(f"✅ NewsAPI から {len(articles)} 件の記事を取得")
        return articles[:5]  # 最新5件取得
    except requests.Timeout:
        print("❌ NewsAPI リクエストがタイムアウトしました。")
        return []
    except Exception as e:
        print(f"⚠️ NewsAPI 取得中にエラー発生: {e}")
        return []


def generate_news_summary(title_en, description_en):
    """Gemini API を使ってニュース記事を生成（タイトルも日本語に翻訳）"""
    if not title_en.strip() or not description_en.strip():
        print("⚠️ タイトルまたは概要が空のためスキップ")
        return "タイトルなし", "内容なし"

    prompt = f"""
    以下の英語のニュースタイトルと概要を基に、日本語で記事を作成してください。
    1. タイトルを適切な日本語に翻訳する
    2. 概要を基に日本語で詳細なニュース記事を書く
    3. 元の英語のテキストは含めない
    4. 必要な情報を補完しつつ、読みやすい文章にする

    タイトル: {title_en}
    概要: {description_en}

    【出力フォーマット】
    タイトル: (ここに日本語タイトル)
    記事: (ここに日本語ニュース記事)
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        print(f"⏳ Gemini API にリクエスト送信中... (タイトル: {title_en[:30]}...)")
        start_time = time.time()
        response = model.generate_content(prompt, generation_config={"max_output_tokens": 500})
        elapsed_time = time.time() - start_time
        print(f"✅ Gemini API 応答取得（{elapsed_time:.2f}秒）")

        # レスポンスの検証
        if not response or not hasattr(response, "candidates") or not response.candidates:
            print("❌ Gemini API の応答が不正または空です。")
            return "記事生成エラー", "Gemini API の応答が空です。"

        # Gemini API のレスポンス解析
        content = response.candidates[0].content
        if hasattr(content, "parts") and content.parts:
            summary_text = content.parts[0].text.strip()  # 正しいフィールドを取得
        else:
            print(f"❌ Gemini API のレスポンスが空です。実際のレスポンス: {response.candidates[0]}")
            return "コンテンツエラー", "コンテンツエラー"

        # タイトルと本文を分割
        lines = summary_text.split("\n")
        title_ja = lines[0].replace("タイトル:", "").strip() if len(lines) > 0 else "翻訳エラー"
        article_ja = "\n".join(lines[1:]).replace("記事:", "").strip() if len(lines) > 1 else "要約エラー"

        return title_ja, article_ja
    except Exception as e:
        print(f"❌ Gemini API でエラー発生: {e}")
        return "Gemini API エラー", str(e)

def create_pdf(content, filename="news_summary.pdf"):
    """ニュースの要約をPDFファイルとして保存"""
    try:
        html_content = f"""
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: "Arial", sans-serif; line-height: 1.6; }}
            h1 {{ color: #333; text-align: center; }}
            h2 {{ color: #555; }}
            p {{ font-size: 14px; }}
            .article {{ border-bottom: 1px solid #ddd; padding-bottom: 10px; margin-bottom: 10px; }}
        </style>
        </head>
        <body>
        <h1>📰 今日のニュース要約</h1>
        {content}
        </body>
        </html>
        """
        HTML(string=html_content).write_pdf(filename)
        print(f"📄 PDFファイル作成成功: {filename}")
        return filename
    except Exception as e:
        print(f"⚠️ PDF作成に失敗しました: {e}")
        return None

def send_email(pdf_filename):
    """生成したPDFをGmailで送信"""
    try:
        msg = EmailMessage()
        msg["Subject"] = "📩 今日のニュース要約"
        msg["From"] = GMAIL_USER
        msg["To"] = GMAIL_RECEIVER
        msg.set_content("今日のニュースを要約しました。添付PDFをご確認ください。")

        with open(pdf_filename, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=pdf_filename)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)

        print(f"📧 メール送信成功: {GMAIL_RECEIVER}")
    except Exception as e:
        print(f"⚠️ メール送信に失敗しました: {e}")

def main():
    print("📡 最新ニュースを取得中...")
    articles = get_latest_news()

    if not articles:
        print("❌ ニュース記事が取得できませんでした。")
        return

    news_summary = ""

    for article in articles:
        title_en = article.get("title", "タイトルなし")
        description_en = article.get("description", "概要なし")
        url = article.get("url", "")

        title_ja, summary = generate_news_summary(title_en, description_en)

        news_summary += f"<h2>📰 {title_ja}</h2><p>{summary}</p><p>🔗 <a href='{url}'>{url}</a></p>"

    pdf_filename = create_pdf(news_summary)
    if pdf_filename:
        send_email(pdf_filename)

if __name__ == "__main__":
    main()