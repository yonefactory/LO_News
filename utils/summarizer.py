import openai
import os
import requests
from bs4 import BeautifulSoup

# OpenAI API 클라이언트 설정
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate_title(title):
    """영어 제목을 한국어로 번역"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Translate the following news title into Korean."},
                {"role": "user", "content": title}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"번역 오류: {e}"

def summarize_article(url):
    """기사 본문을 5문장으로 요약, 각 문장을 불릿 포인트로 표시"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.select("p")
        full_text = " ".join([p.text for p in paragraphs if p.text.strip()])

        if not full_text:
            return "요약할 내용이 부족합니다."

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize the following article in 5 sentences in Korean."},
                {"role": "user", "content": full_text}
            ]
        )

        summary = response.choices[0].message.content.strip()

        # ✅ 요약된 문장을 개별 문장으로 분리하여 불릿 리스트로 변환
        bullet_summary = "\n".join([f"- {sentence.strip()}" for sentence in summary.split(". ") if sentence])

        return bullet_summary

    except Exception as e:
        return f"요약 오류: {e}"
