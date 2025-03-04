import openai
import os
import requests
from bs4 import BeautifulSoup

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_title(title):
    """영어 제목을 한국어로 번역"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Translate the following news title into Korean."},
                {"role": "user", "content": title}
            ]
        )

        # ✅ 최신 API 방식으로 결과 추출
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"번역 오류: {e}"

def summarize_article(url):
    """기사 본문을 5문장으로 요약"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.select("p")
        full_text = " ".join([p.text for p in paragraphs if p.text.strip()])

        if not full_text:
            return "요약할 내용이 부족합니다."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize the following article in 5 sentences in Korean."},
                {"role": "user", "content": full_text}
            ]
        )

        # ✅ 최신 API 방식으로 결과 추출
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"요약 오류: {e}"
