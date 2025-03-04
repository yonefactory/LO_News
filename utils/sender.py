import smtplib
import requests
from email.mime.text import MIMEText
from utils.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVERS, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS

def send_email(news_summary):
    msg = MIMEText(news_summary, "plain", "utf-8")
    msg["Subject"] = "오늘의 Apple 뉴스"
    msg["From"] = EMAIL_SENDER

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        for recipient in EMAIL_RECEIVERS:
            msg["To"] = recipient
            server.sendmail(EMAIL_SENDER, recipient, msg.as_string())

def send_telegram(news_summary):
    message = f"📢 오늘의 Apple 뉴스 📢\n\n{news_summary}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    for chat_id in TELEGRAM_CHAT_IDS:
        payload = {"chat_id": chat_id, "text": message}
        requests.post(url, json=payload)
