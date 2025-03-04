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
    # 최신 뉴스 가져오기
    articles = get_latest_news()

    # 뉴스 포맷팅
    news_summary = format_news(articles)

    # 이메일 및 텔레그램으로 전송
    send_email(news_summary)
    send_telegram(news_summary)
