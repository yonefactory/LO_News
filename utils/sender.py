import smtplib
import requests
from email.mime.text import MIMEText
from utils.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVERS, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS

# 이메일 SMTP 설정
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(news_summary):
    """이메일 전송 (UTF-8 인코딩 사용)"""
    try:
        print("🟢 [DEBUG] 이메일 전송 시작")

        # 이메일 제목 설정
        subject = "오늘의 Apple 뉴스"
    
        # SMTP 서버에 연결
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            for recipient in EMAIL_RECEIVERS:
                # 각 수신자마다 새로운 MIMEText 객체 생성
                msg = MIMEText(news_summary, "plain", "utf-8")
                msg["Subject"] = subject
                msg["From"] = EMAIL_SENDER
                msg["To"] = recipient
    except smtplib.SMTPAuthenticationError:
        print("❌ [ERROR] SMTP 로그인 인증 실패! 이메일/비밀번호 또는 앱 비밀번호 확인 필요.")
    except smtplib.SMTPConnectError:
        print("❌ [ERROR] SMTP 서버 연결 실패! 네트워크 상태 확인 필요.")
    except smtplib.SMTPException as e:
        print(f"❌ [ERROR] SMTP 오류 발생: {e}")
    except Exception as e:
        print(f"❌ [ERROR] 알 수 없는 이메일 전송 오류: {e}")

def send_telegram(news_summary):
    """텔레그램 메시지 전송 (디버깅 추가)"""
    try:
        print("🟢 [DEBUG] 텔레그램 메시지 전송 시작")

        message = news_summary
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        for chat_id in TELEGRAM_CHAT_IDS:
            payload = {"chat_id": chat_id, "text": message}
            print(f"🟢 [DEBUG] {chat_id}에게 텔레그램 메시지 전송 중...")

            response = requests.post(url, json=payload)

            # 응답 상태 코드 확인 (200이 아니면 실패 출력)
            if response.status_code == 200:
                print(f"✅ [INFO] 텔레그램 메시지가 {chat_id}에게 성공적으로 전송되었습니다.")
            else:
                print(f"⚠️ [WARNING] 텔레그램 메시지 전송 실패 (채팅 ID: {chat_id}): {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ [ERROR] 텔레그램 API 연결 실패! 네트워크 상태 확인 필요.")
    except requests.exceptions.Timeout:
        print("❌ [ERROR] 텔레그램 API 요청 시간 초과!")
    except requests.exceptions.RequestException as e:
        print(f"❌ [ERROR] 텔레그램 메시지 전송 중 오류 발생: {e}")
