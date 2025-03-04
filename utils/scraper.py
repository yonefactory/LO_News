import requests
from bs4 import BeautifulSoup
from utils.summarizer import translate_title, summarize_article

def fetch_news_from_site(url, title_selector, link_selector, base_url=""):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for title_tag, link_tag in zip(soup.select(title_selector), soup.select(link_selector)):
        title = title_tag.text.strip()
        link = link_tag.get("href", "")
        if not link.startswith("http"):
            link = base_url + link
        translated_title = translate_title(title)
        summary = summarize_article(link)
        articles.append({"title": translated_title, "link": link, "summary": summary})

    return articles

def get_latest_news():
    news_sources = [
        {"url": "https://9to5mac.com/", "title_selector": "h2 a", "link_selector": "h2 a", "base_url": ""},
        {"url": "https://www.macrumors.com/", "title_selector": ".title a", "link_selector": ".title a", "base_url": "https://www.macrumors.com"},
        {"url": "https://www.apple.com/kr/newsroom/", "title_selector": ".headline a", "link_selector": ".headline a", "base_url": "https://www.apple.com"},
        {"url": "https://kr.investing.com/equities/apple-computer-inc-news", "title_selector": ".textDiv a.title", "link_selector": ".textDiv a.title", "base_url": "https://kr.investing.com"}
    ]

    all_articles = []
    seen_titles = set()

    for source in news_sources:
        articles = fetch_news_from_site(source["url"], source["title_selector"], source["link_selector"], source["base_url"])
        for article in articles:
            if article["title"] not in seen_titles:
                seen_titles.add(article["title"])
                all_articles.append(article)

    return all_articles
