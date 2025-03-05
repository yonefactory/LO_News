import json
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

SENT_ARTICLES_FILE = "sent_articles.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

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

def fetch_news_from_site(url, title_selector, link_selector, base_url="", limit=1, use_selenium=False):
    """특정 사이트에서 최신 뉴스 크롤링 (JavaScript 필요 시 Selenium 사용)"""
    articles = []
    
    if use_selenium:
        options = Options()
        options.add_argument("--headless")  # 창 없이 실행
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        html = driver.page_source
        driver.quit()
    else:
        response = requests.get(url, headers=HEADERS)
        html = response.text

    soup = BeautifulSoup(html, "html.parser")

    for title_tag, link_tag in zip(soup.select(title_selector), soup.select(link_selector)):
        title = title_tag.text.strip()
        link = link_tag.get("href", "")
        if not link.startswith("http"):
            link = base_url + link
        articles.append({"title": title, "link": link})

        if len(articles) >= limit:
            break

    return articles

def get_latest_news(test_mode=False):
    """최신 뉴스 가져오기 (중복 방지)"""
    news_sources = [
        {"url": "https://9to5mac.com/", "title_selector": "h2 a", "link_selector": "h2 a", "base_url": "", "use_selenium": False},
        {"url": "https://www.macrumors.com/", "title_selector": ".post-title a", "link_selector": ".post-title a", "base_url": "https://www.macrumors.com", "use_selenium": False},
        {"url": "https://www.apple.com/kr/newsroom/", "title_selector": "a.headline", "link_selector": "a.headline", "base_url": "https://www.apple.com", "use_selenium": True},
        {"url": "https://kr.investing.com/equities/apple-computer-inc-news", "title_selector": "a.title", "link_selector": "a.title", "base_url": "https://kr.investing.com", "use_selenium": True}
    ]

    all_articles = []
    sent_articles = load_sent_articles()

    for source in news_sources:
        print(f"🔍 [DEBUG] '{source['url']}' 사이트에서 기사 추출 시작...")
        articles = fetch_news_from_site(
            source["url"],
            source["title_selector"],
            source["link_selector"],
            source["base_url"],
            limit=1 if test_mode else 5,
            use_selenium=source.get("use_selenium", False)
        )

        print(f"📰 [DEBUG] '{source['url']}' 사이트에서 {len(articles)}개의 기사 추출 완료:")
        for article in articles:
            print(f"    - 제목: {article['title']}")
            print(f"      링크: {article['link']}")
            if article["link"] not in sent_articles:
                sent_articles.append(article["link"])
                all_articles.append(article)

    save_sent_articles(sent_articles)
    return all_articles
