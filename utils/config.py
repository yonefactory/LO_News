import os
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# GitHub Secrets에서 불러오기
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# config.ini에서 불러오기 (다수의 이메일 & 텔레그램 ID)
EMAIL_RECEIVERS = [email.strip() for email in config["EMAIL"]["RECEIVERS"].split(",")]
TELEGRAM_CHAT_IDS = [chat_id.strip() for chat_id in config["TELEGRAM"]["CHAT_IDS"].split(",")]
