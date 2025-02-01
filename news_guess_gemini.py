import os
import sys
import google.generativeai as genai
import requests
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from weasyprint import HTML

# PyCharm の print バッファリングを回避
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

# グローバル変数（初期化）
NEWSAPI_KEY = None
GEMINI_API_KEY = None
GMAIL_USER = None
GMAIL_PASS = None
GMAIL_RECEIVER = None


# .envファイルはルートディレクトリに配置
def load_environment():
    """環境変数のロード"""
    load_dotenv()


def validate_env():
    """環境変数の検証"""
    required_keys = ["NEWSAPI_KEY", "GEMINI_API_KEY", "GMAIL_USER", "GMAIL_PASS", "GMAIL_RECEIVER"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        raise ValueError(f"❌ 以下の環境変数が見つかりません: {', '.join(missing_keys)}")


def configure_api():
    """API のセットアップ"""
    global NEWSAPI_KEY, GEMINI_API_KEY, GMAIL_USER, GMAIL_PASS, GMAIL_RECEIVER
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GMAIL_USER = os.getenv("GMAIL_USER")
    GMAIL_PASS = os.getenv("GMAIL_PASS")
    GMAIL_RECEIVER = os.getenv("GMAIL_RECEIVER")
    genai.configure(api_key=GEMINI_API_KEY)


def get_latest_news(max_articles):
    """NewsAPI から記事を取得"""
    url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&pageSize={max_articles}&apiKey={NEWSAPI_KEY}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("status") != "ok":
            raise ValueError(f"⚠️ NewsAPI エラー: {data.get('message')}")
        return data.get("articles", [])
    except requests.RequestException as e:
        raise RuntimeError(f"❌ NewsAPI 取得中にエラー発生: {e}")


def extract_element(article):
    """記事からタイトル、概要、本文、URL を取得"""
    return (
        article.get("title") or "タイトルなし",
        article.get("description") or "概要なし",
        article.get("content") or "本文なし",  # `None` の場合も "本文なし" にする
        article.get("url") or ""
    )


def generate_news_summary(title_en, description_en, content_en):
    """Gemini API を使ってニュース記事を日本語で要約"""

    if not title_en.strip():
            title_en = "タイトルなし"
    if not description_en.strip():
            description_en = "概要なし"
    if not content_en.strip():
            content_en = "本文なし"

    prompt = f"""
    以下の英語のニュースタイトルと概要と本文を基に、記事内容を要約してわかりやすく教えて

    **条件**
    1. タイトルを **自然な日本語に翻訳** する
    2. 概要と本文を基に **日本語の詳細なニュース要約** を作成する
    3. **シンプルで分かりやすい文章** にする
    4. **元の英語のテキストは含めない**

    **入力**
    - タイトル: {title_en}
    - 概要: {description_en}
    - 本文: {content_en}

    **出力フォーマット**
    タイトル: (ここに日本語タイトル)
    記事: (ここに日本語ニュース要約)
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt, generation_config={"max_output_tokens": 500})
        content = response.candidates[0].content.parts[0].text.strip()
        lines = content.split("\n")
        title_ja = lines[0].replace("タイトル:", "").strip() if len(lines) > 0 else "翻訳エラー"
        article_ja = "\n".join(lines[1:]).replace("記事:", "").strip() if len(lines) > 1 else "要約エラー"
        return title_ja, article_ja
    except Exception as e:
        return "Gemini API エラー", str(e)


def process_articles(articles):
    """記事を処理してHTMLフォーマットの文字列を作成"""
    content = ""
    for article in articles:
        title, summary = generate_news_summary(*extract_element(article)[:3])  # ✅ 1回だけ呼ぶ

        content += f"<h2>📰 {title}</h2>"
        content += f"<p>{summary}</p>"
        content += f"<p>🔗 <a href='{extract_element(article)[3]}'>{extract_element(article)[3]}</a></p>"

    return content


def create_pdf(content, filename="news_summary.pdf"):
    """ニュースの要約をPDFファイルとして保存"""
    try:
        HTML(
            string=f"<html><head><meta charset='UTF-8'></head><body><h1>📰 今日のニュース要約</h1>{content}</body></html>").write_pdf(
            filename)
        return filename
    except Exception as e:
        raise RuntimeError(f"⚠️ PDF作成に失敗しました: {e}")


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
    except Exception as e:
        raise RuntimeError(f"⚠️ メール送信に失敗しました: {e}")


def main():
    try:
        load_environment()
        validate_env()
        configure_api()
        articles = get_latest_news(max_articles=5)
        if not articles:
            print("❌ ニュース記事が取得できませんでした。")
            return
        pdf_filename = create_pdf(process_articles(articles))
        send_email(pdf_filename)
    except Exception as e:
        print(f"⚠️ エラー発生: {e}")


if __name__ == "__main__":
    main()
