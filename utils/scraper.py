import json
import os
import requests
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
    """특정 사이트에서 최신 뉴스 크롤링 (테스트 모드에서는 limit=1 적용)"""
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

        if len(articles) >= limit:  # ✅ 테스트 모드에서는 최근 1개만 가져오기
            break

    return articles

def get_latest_news(test_mode=False):
    """최신 뉴스 가져오기 (중복 방지)"""
    news_sources = [
        {"url": "https://9to5mac.com/", "title_selector": "a.title", "link_selector": "a.title", "base_url": ""},
        {"url": "https://www.macrumors.com/", "title_selector": "a.title", "link_selector": "a.title", "base_url": "https://www.macrumors.com"},
        {"url": "https://www.apple.com/kr/newsroom/", "title_selector": "a.headline", "link_selector": "a.headline", "base_url": "https://www.apple.com"},
        {"url": "https://kr.investing.com/equities/apple-computer-inc-news", "title_selector": "a.title", "link_selector": "a.title", "base_url": "https://kr.investing.com"}
    ]

    all_articles = []
    sent_articles = load_sent_articles()  # ✅ 이미 보낸 기사 목록 불러오기

    for source in news_sources:
        print(f"🔍 [DEBUG] '{source['url']}' 사이트에서 기사 추출 시작...")
        articles = fetch_news_from_site(
            source["url"],
            source["title_selector"],
            source["link_selector"],
            source["base_url"],
            limit=1 if test_mode else 5  # ✅ 테스트 모드일 때는 1개만 가져오기
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
