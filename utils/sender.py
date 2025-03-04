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
        # 이메일 메시지 설정 (MIME)
        msg = MIMEMultipart()
        msg["Subject"] = "오늘의 Apple 뉴스"
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(EMAIL_RECEIVERS)  # 여러 수신자를 콤마(,)로 구분

        # 이메일 본문을 UTF-8로 설정
        msg.attach(MIMEText(news_summary, "plain", "utf-8"))

        # SMTP 서버에 연결하여 이메일 전송
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVERS, msg.as_string())

        print("✅ 이메일 전송 완료!")

    except Exception as e:
        print(f"❌ 이메일 전송 오류: {e}")
