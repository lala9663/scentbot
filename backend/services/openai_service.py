from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import json

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

load_dotenv()
BASE_PROMPT = """
당신은 향수 전문가 AI입니다.

반드시 JSON만 반환하세요.

응답 형식:

{
  "type": "recommendation",
  "message": "",
  "recommendations": [
    { "name": "", "brand": "", "reason": "" }
  ],
  "blogs": [
    { "title": "" },
    { "title": "" },
    { "title": "" }
  ]
}

규칙:
- 반드시 JSON만 반환
- 한국어 사용
- 추천은 자연스럽게
- 🔥 블로그는 실제 링크 생성 금지 (제목만)
- 🔥 블로그는 추천과 관련된 주제 3개 생성
"""




def build_system_prompt(collection, wishlist, perfumes):
    prompt = BASE_PROMPT

    # 🔥 DB 기반 추천 후보
    if perfumes:
        perfume_text = "\n".join(
            f"- {p.get('name', 'Unknown')}: {p.get('description', '')}"
            for p in perfumes
        )

        prompt += f"""

추천 후보 향수 목록:
{perfume_text}

반드시 위 목록 안에서만 추천하세요.
"""

    # 🔥 컬렉션
    if collection:
        col_text = "\n".join(
            f"- {c.get('name')} ({c.get('brand', '')})"
            for c in collection
        )

        prompt += f"""

사용자의 보유 향수:
{col_text}

가능하면 보유 향수를 우선 고려하세요.
"""

    # 🔥 위시리스트
    if wishlist:
        wish_text = "\n".join(
            f"- {w.get('name')} ({w.get('brand', '')})"
            for w in wishlist
        )

        prompt += f"""

사용자의 위시리스트:
{wish_text}

사용자의 취향을 분석할 때 참고하세요.
"""

    # 🔥 블로그 힌트 (핵심 추가)
    prompt += """

추천 결과와 함께 관련된 블로그 주제 3개를 생성하세요.
- 실제 링크 생성 금지
- 제목 형태로만 작성
- 사용자가 읽어보고 싶게 자연스럽게 작성
"""

    return prompt

async def get_perfume_response(query, perfumes, collection, wishlist):
    system_prompt = build_system_prompt(collection, wishlist, perfumes)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content


async def generate_perfume_data(query: str):
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """
반드시 아래 JSON 형식으로 반환:

{
  "name": "",
  "description": "",
  "notes": {
    "top": [],
    "middle": [],
    "base": []
  }
}
"""
            },
            {"role": "user", "content": query}
        ],
        response_format={"type": "json_object"},
    )

    data = json.loads(response.choices[0].message.content)

    return {
        "name": data.get("name", query),
        "description": data.get("description", ""),
        "notes": data.get("notes", {"top": [], "middle": [], "base": []})
    }


async def generate_perfume_data(query: str):
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "향수 정보를 JSON으로 생성"},
            {"role": "user", "content": query}
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)