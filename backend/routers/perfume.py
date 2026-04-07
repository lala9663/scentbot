from fastapi import APIRouter
import httpx

router = APIRouter()


@router.get("/perfume/image")
async def get_perfume_image(name: str, brand: str = ""):
    """
    향수 이름으로 Brave Image Search API 또는 DuckDuckGo에서 대표 이미지를 가져옵니다.
    API 키 없이 쓸 수 있는 DuckDuckGo 방식 사용.
    """
    query = f"{brand} {name} perfume bottle".strip()
    url = f"https://duckduckgo.com/?q={query}&iax=images&ia=images"

    # DuckDuckGo vqd 토큰 먼저 획득
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(
                "https://duckduckgo.com/",
                params={"q": query, "iax": "images", "ia": "images"},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=5,
            )
            vqd = ""
            for line in res.text.split("\n"):
                if "vqd=" in line:
                    vqd = line.split("vqd=")[1].split("&")[0].strip("'\"")
                    break

            if not vqd:
                return {"imageUrl": None}

            img_res = await client.get(
                "https://duckduckgo.com/i.js",
                params={"q": query, "vqd": vqd, "f": ",,,,,", "p": "1"},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=5,
            )
            data = img_res.json()
            results = data.get("results", [])
            if results:
                return {"imageUrl": results[0].get("image")}
            return {"imageUrl": None}

        except Exception:
            return {"imageUrl": None}
