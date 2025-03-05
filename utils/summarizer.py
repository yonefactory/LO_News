import openai
import os
import requests
from bs4 import BeautifulSoup

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_title(title):
    """영어 뉴스 제목을 한국어로 번역"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # 모델을 gpt-4o-mini로 설정
            messages=[
                {"role": "system", "content": "다음 뉴스 제목을 한국어로 번역하세요."},
                {"role": "user", "content": title}
            ]
        )
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
            model="gpt-4o-mini",  # 모델을 gpt-4o-mini로 설정
            messages=[
                {
                    "role": "system",
                    "content": (
                        "다음 기사의 내용을 한국어로 5문장으로 요약하세요. "
                        "간결하고 정확한 문장으로 정리하고, 불필요한 수식어는 제외하세요."
                    )
                },
                {"role": "user", "content": full_text}
            ]
        )

        summary = response.choices[0].message.content.strip()

        # 불릿 포인트 적용하여 가독성 향상
        bullet_summary = "\n".join([f"- {sentence.strip()}" for sentence in summary.split(". ") if sentence])

        return bullet_summary

    except Exception as e:
        return f"요약 오류: {e}"
