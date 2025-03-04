import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header  # ✅ 제목 UTF-8 인코딩을 위한 모듈 추가
from utils.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVERS, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS

# 이메일 SMTP 설정
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(news_summary):
    """이메일 전송 (UTF-8 인코딩 적용 + 디버깅)"""
    try:
        print("🟢 [DEBUG] 이메일 전송 시작")

        # ✅ 이메일 메시지 객체 생성
        msg = MIMEMultipart()
        
        # ✅ 제목을 UTF-8로 인코딩하여 설정
        msg["Subject"] = "오늘의 Apple 뉴스"
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(EMAIL_RECEIVERS)

        # ✅ 이메일 본문 UTF-8 인코딩 설정
        #body = MIMEText(news_summary, "plain", "utf-8")
        body = "body"
        msg.attach(body)

        print("🟢 [DEBUG] 이메일 객체 생성 완료")

        # ✅ SMTP 서버 연결 및 이메일 전송
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            print("🟢 [DEBUG] SMTP 서버 연결 시도 중...")
            server.ehlo()
            server.starttls()
            server.ehlo()
            print("🟢 [DEBUG] TLS 보안 활성화 완료")

            print("🟢 [DEBUG] SMTP 로그인 시도 중...")
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            print("🟢 [DEBUG] SMTP 로그인 성공")

            print("🟢 [DEBUG] 이메일 전송 시도 중...")
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVERS, msg.as_string())
            print("✅ 이메일 전송 완료!")

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

        message = f"📢 오늘의 Apple 뉴스 📢\n\n{news_summary}"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        for chat_id in TELEGRAM_CHAT_IDS:
            payload = {"chat_id": chat_id, "text": message}
            print(f"🟢 [DEBUG] {chat_id}에게 텔레그램 메시지 전송 중...")

            response = requests.post(url, json=payload)

            # ✅ 응답 상태 코드 확인 (200이 아니면 실패 출력)
            if response.status_code != 200:
                print(f"⚠️ [WARNING] 텔레그램 메시지 전송 실패 (채팅 ID: {chat_id}): {response.text}")

            response.raise_for_status()

        print("✅ 텔레그램 메시지 전송 완료!")

    except requests.exceptions.ConnectionError:
        print("❌ [ERROR] 텔레그램 API 연결 실패! 네트워크 상태 확인 필요.")
    except requests.exceptions.Timeout:
        print("❌ [ERROR] 텔레그램 API 요청 시간 초과!")
    except requests.exceptions.RequestException as e:
        print(f"❌ [ERROR] 텔레그램 메시지 전송 중 오류 발생: {e}")
