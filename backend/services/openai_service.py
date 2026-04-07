from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_PROMPT = """
당신은 향수 전문가 AI입니다.

사용자가 향수 이름을 말하면 아래 JSON 형식으로만 응답하세요.
다른 설명이나 마크다운 없이 JSON만 반환하세요.

{
  "type": "perfume_info",
  "name": "향수 전체 이름",
  "brand": "브랜드명",
  "perfumeType": "EDP",
  "imageUrl": "해당 향수의 공식 제품 이미지 URL. 확실하지 않으면 null",
  "notes": {
    "top": ["노트1", "노트2"],
    "middle": ["노트1", "노트2"],
    "base": ["노트1", "노트2"]
  },
  "season": ["봄", "가을"],
  "occasion": ["포멀", "데일리"],
  "mood": "우디 아로마틱",
  "similar": ["비슷한 향수1", "비슷한 향수2", "비슷한 향수3"],
  "description": "이 향수의 감성을 한두 문장으로 설명"
}

향수 추천 요청 (느낌, 계절, 상황 등)이 오면 아래 형식으로 응답하세요.

{
  "type": "recommendation",
  "message": "추천 이유를 친근하게 설명",
  "recommendations": [
    { "name": "향수명", "brand": "브랜드", "reason": "추천 이유 한 줄" },
    { "name": "향수명", "brand": "브랜드", "reason": "추천 이유 한 줄" },
    { "name": "향수명", "brand": "브랜드", "reason": "추천 이유 한 줄" }
  ]
}

일반 대화나 향수 관련 질문은 아래 형식으로 응답하세요.

{
  "type": "message",
  "message": "친근하고 자연스러운 한국어 답변"
}

규칙:
- 반드시 JSON만 반환, 마크다운 코드블록 사용 금지
- 모든 응답은 한국어로
- 향수 노트는 한국어로 번역해서 반환
- imageUrl은 실제로 접근 가능한 공식 이미지 URL만 반환, 확실하지 않으면 null
"""


def build_system_prompt(collection: list, wishlist: list) -> str:
    prompt = BASE_PROMPT

    if collection:
        col_text = "\n".join(
            f"- {c['name']} ({c.get('brand', '')}, {c.get('perfumeType', '')}{', ' + str(c['ml']) + 'ml' if c.get('ml') else ''})"
            for c in collection
        )
        prompt += f"""
---
사용자의 보유 향수 컬렉션:
{col_text}

추천 요청 시 컬렉션에 있는 향수를 우선적으로 고려하세요.
"내가 가진 향수 중에서" 라는 요청이 오면 반드시 컬렉션 내에서만 추천하세요.
"""

    if wishlist:
        wish_text = "\n".join(
            f"- {w['name']} ({w.get('brand', '')}, {w.get('perfumeType', '')})"
            for w in wishlist
        )
        prompt += f"""
---
사용자의 위시리스트 (갖고 싶은 향수):
{wish_text}

위시리스트 향수에 대해 질문하면 사용자가 관심 있는 향수임을 인지하고 답변하세요.
취향 분석 시 위시리스트도 참고하세요.
"""

    return prompt


async def get_perfume_response(messages: list, collection: list, wishlist: list) -> str:
    system_prompt = build_system_prompt(collection, wishlist)

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_prompt}] + messages,
        temperature=0.7,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content