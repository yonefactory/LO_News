from utils.scraper import get_latest_news
from utils.sender import send_email, send_telegram

def format_news(articles):
    """뉴스를 보기 좋은 형식으로 정리"""
    formatted_news = "📢 오늘의 Apple 뉴스 📢\n"
    for article in articles:
        formatted_news += f"\n📌 {article['title']}\n"
        formatted_news += f"📝 {article['summary']}\n"
        formatted_news += f"🔗 {article['link']}\n"
    return formatted_news

if __name__ == "__main__":
    articles = get_latest_news()
    news_summary = format_news(articles)

    # ✅ 디버깅: 전송할 메시지를 먼저 출력하여 확인
    print("\n===================== 📩 이메일 & 텔레그램 전송 전 미리보기 =====================")
    print(news_summary)
    print("=================================================================================\n")

    send_email(news_summary)  # ✅ 이메일 전송
    send_telegram(news_summary)  # ✅ 텔레그램 전송
