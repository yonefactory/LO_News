import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVERS, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(news_summary):
    """이메일 전송 (UTF-8 인코딩 설정)"""
    try:
        # 이메일 메시지 객체 생성
        msg = MIMEMultipart()
        msg["Subject"] = "오늘의 Apple 뉴스"
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(EMAIL_RECEIVERS)  # 여러 명에게 전송

        # 이메일 본문을 UTF-8로 인코딩하여 추가
        body = MIMEText(news_summary, "plain", "utf-8")
        msg.attach(body)

        # SMTP 서버에 연결하여 이메일 전송
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVERS, msg.as_string().encode("utf-8"))

        print("✅ 이메일 전송 완료!")

    except Exception as e:
        print(f"❌ 이메일 전송 오류: {e}")

def send_telegram(news_summary):
    """텔레그램 메시지 전송"""
    try:
        message = f"📢 오늘의 Apple 뉴스 📢\n\n{news_summary}"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        for chat_id in TELEGRAM_CHAT_IDS:
            payload = {"chat_id": chat_id, "text": message}
            response = requests.post(url, json=payload)
            response.raise_for_status()

        print("✅ 텔레그램 메시지 전송 완료!")

    except Exception as e:
        print(f"❌ 텔레그램 전송 오류: {e}")
