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

def refine_text(text):
    """구어체 문장을 문어체 뉴스 형식으로 변환"""
    replacements = {
        "했습니다": "했다", "합니다": "", "됩니다": "", "될 것입니다": "된다", "제공됩니다": "제공",
        "출시되었습니다": "출시", "예고되었습니다": "예고", "탑재되었습니다": "탑재", "진행됩니다": "진행",
        "공개되었습니다": "공개", "예정입니다": "예정", "향상되었습니다": "향상", "강화되었습니다": "강화"
    }
    
    for key, value in replacements.items():
        text = text.replace(key, value)

    return text

def summarize_article(url):
    """기사 본문을 뉴스 형식(문어체)으로 5문장 요약"""
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
                {
                    "role": "system",
                    "content": (
                        "Summarize the following article in 5 sentences in Korean. "
                        "Use a formal, concise, and factual style suitable for a news article. "
                        "Ensure that no conversational expressions are used. "
                        "Do NOT use endings like '했습니다', '합니다', '예정입니다', '될 것입니다'. "
                        "Instead, state facts directly without unnecessary verb endings. "
                        "For example:\n"
                        "- '팀 쿡은 새로운 제품을 발표했습니다.' → '팀 쿡, 새로운 제품 발표'\n"
                        "- '이번 업데이트에서는 배터리 성능이 향상되었습니다.' → '배터리 성능 향상'\n"
                        "- '출시될 예정입니다.' → '출시 예정'\n"
                        "Summarize the article while strictly following this rule."
                    )
                },
                {"role": "user", "content": full_text}
            ]
        )

        summary = response.choices[0].message.content.strip()
        
        # ✅ 구어체 잔여 표현 제거 후 반환
        refined_summary = refine_text(summary)

        # ✅ 불릿 포인트 적용하여 가독성 향상
        bullet_summary = "\n".join([f"- {sentence.strip()}" for sentence in refined_summary.split(". ") if sentence])

        return bullet_summary

    except Exception as e:
        return f"요약 오류: {e}"
