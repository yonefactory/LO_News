import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVERS, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(news_summary):
    """이메일 전송 (UTF-8 인코딩 문제 해결)"""
    try:
        # 이메일 메시지 객체 생성 (UTF-8 설정)
        msg = MIMEMultipart()
        msg["Subject"] = "=?UTF-8?B?" + MIMEText("오늘의 Apple 뉴스", "plain", "utf-8").as_string() + "?="
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(EMAIL_RECEIVERS)  # 여러 수신자 지원

        # 이메일 본문을 UTF-8로 설정
        body = MIMEText(news_summary, "plain", "utf-8")
        msg.attach(body)

        # SMTP 서버 연결 및 이메일 전송
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVERS, msg.as_string())  # ✅ UTF-8 자동 처리됨

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
