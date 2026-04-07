from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.openai_service import get_perfume_response

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
    messages = [m.model_dump() for m in req.messages]
    collection = [c.model_dump() for c in req.collection]
    wishlist = [w.model_dump() for w in req.wishlist]
    reply = await get_perfume_response(messages, collection, wishlist)
    return {"reply": reply}
