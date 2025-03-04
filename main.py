from utils.scraper import get_latest_news
from utils.sender import send_email, send_telegram
import os
import sys

# ✅ GitHub Actions에서 환경 변수로 전달받은 TEST_MODE 값 적용
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true" or "--test" in sys.argv

def format_news(articles):
    """뉴스를 보기 좋은 형식으로 정리"""
    formatted_news = "📢 오늘의 Apple 뉴스 📢\n"
    for article in articles:
        formatted_news += f"\n📌 {article['title']}\n"
        formatted_news += f"{article['summary']}\n"
        formatted_news += f"🔗 {article['link']}\n"
    return formatted_news

def format_news_only_text(articles):
    """뉴스를 보기 좋은 형식으로 정리"""
    formatted_news = "오늘의 Apple 뉴스\n"
    for article in articles:
        formatted_news += f"\n{article['title']}\n"
        formatted_news += f"{article['summary']}\n"
        #formatted_news += f"{article['link']}\n"
    return formatted_news

if __name__ == "__main__":
    articles = get_latest_news(test_mode=TEST_MODE)

    if not articles:
        print("⚠️ 새로운 기사가 없으므로 전송하지 않습니다.")
        sys.exit(0)  # ✅ 새로운 기사가 없으면 실행 종료

    news_summary = format_news(articles)

    # ✅ 디버깅: 전송할 메시지를 먼저 출력하여 확인
    print("\n===================== 📩 이메일 & 텔레그램 전송 전 미리보기 =====================")
    print(news_summary)
    print("=================================================================================\n")

    send_email(news_summary)  # ✅ 이메일 전송
    send_telegram(news_summary)  # ✅ 텔레그램 전송
