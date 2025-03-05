import json
import os
import requests
import feedparser  # RSS 피드 파싱을 위한 라이브러리
from bs4 import BeautifulSoup
from utils.summarizer import translate_title, summarize_article

SENT_ARTICLES_FILE = "sent_articles.json"

def load_sent_articles():
    """전송된 기사 목록을 JSON 파일에서 불러오기"""
    if os.path.exists(SENT_ARTICLES_FILE):
        with open(SENT_ARTICLES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_sent_articles(sent_articles):
    """전송된 기사 목록을 JSON 파일에 저장"""
    with open(SENT_ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump(sent_articles, f, ensure_ascii=False, indent=4)

def fetch_news_from_site(url, title_selector, link_selector, base_url="", limit=1):
    """일반적인 웹 크롤링 방식으로 최신 뉴스 가져오기"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for link_tag in soup.select(link_selector):
        title = link_tag.text.strip()
        link = link_tag.get("href", "")
        if not link.startswith("http"):
            link = base_url + link
        translated_title = translate_title(title)
        summary = summarize_article(link)
        articles.append({"title": translated_title, "link": link, "summary": summary})

        if len(articles) >= limit:
            break

    return articles

def fetch_news_from_rss(rss_url, limit=1):
    """RSS 피드를 사용하여 뉴스 가져오기"""
    feed = feedparser.parse(rss_url)
    articles = []

    for entry in feed.entries[:limit]:  # limit 개수만큼 기사 가져오기
        title = entry.title
        link = entry.link
        translated_title = translate_title(title)
        summary = summarize_article(link)

        articles.append({"title": translated_title, "link": link, "summary": summary})

    return articles

def get_latest_news(test_mode=False):
    """최신 뉴스 가져오기 (중복 방지)"""
    news_sources = [
        {"url": "https://9to5mac.com/", "title_selector": "h2 a", "link_selector": "h2 a", "base_url": "", "use_rss": False},
        {"url": "https://www.macrumors.com/", "rss_url": "https://www.macrumors.com/macrumors.xml", "use_rss": True},
    ]

    all_articles = []
    sent_articles = load_sent_articles()  # ✅ 이미 보낸 기사 목록 불러오기

    for source in news_sources:
        print(f"🔍 [DEBUG] '{source['url']}' 사이트에서 기사 추출 시작...")

        if source.get("use_rss"):
            articles = fetch_news_from_rss(source["rss_url"], limit=1 if test_mode else 5)
        else:
            articles = fetch_news_from_site(
                source["url"],
                source["title_selector"],
                source["link_selector"],
                source["base_url"],
                limit=1 if test_mode else 5
            )
        
        print(f"📰 [DEBUG] '{source['url']}' 사이트에서 {len(articles)}개의 기사 추출 완료:")
        for article in articles:
            print(f"    - 제목: {article['title']}")
            print(f"      링크: {article['link']}")
            if article["link"] not in sent_articles:  # ✅ 이미 보낸 기사와 중복되지 않도록 필터링
                sent_articles.append(article["link"])
                all_articles.append(article)

    save_sent_articles(sent_articles)  # ✅ 새로운 기사 저장
    return all_articles
