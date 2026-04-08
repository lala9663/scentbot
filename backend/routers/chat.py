from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import json
from services.perfume_service import search_similar_perfumes, save_perfume, search_perfume_by_name
from services.openai_service import get_perfume_response, generate_perfume_data

router = APIRouter()


class Message(BaseModel):
    role: str
    content: str


class PerfumeItem(BaseModel):
    name: str
    brand: Optional[str] = None
    perfumeType: Optional[str] = None
    ml: Optional[int] = None


class ChatRequest(BaseModel):
    messages: list[Message]
    collection: Optional[list[PerfumeItem]] = []
    wishlist: Optional[list[PerfumeItem]] = []


@router.post("/chat")
async def chat(req: ChatRequest):
    query = req.messages[-1].content

    collection = [c.model_dump() for c in req.collection]
    wishlist = [w.model_dump() for w in req.wishlist]

    # 🔥 1. GPT 먼저
    reply = await get_perfume_response(query, [], collection, wishlist)

    # 🔥 2. JSON 파싱
    data = json.loads(reply)

    # 🔥 3. 추천일 경우만 처리
    if data.get("type") == "recommendation":
        perfumes = []

        for item in data.get("recommendations", []):
            name = item.get("name")

            # 🔥 DB 검색
            result = search_perfume_by_name(name)

            if result:
                perfumes.append(result)
            else:
                # 🔥 없으면 생성 + 저장
                generated = await generate_perfume_data(name)
                save_perfume(generated)
                perfumes.append(generated)

        # 🔥 GPT 재가공 (선택)
        reply = await get_perfume_response(query, perfumes, collection, wishlist)

    return {"reply": reply}