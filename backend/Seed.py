from services.perfume_service import save_perfume

seed_data = [
{
  "name": "Bleu de Chanel",
  "description": "시트러스와 우디의 조화",
  "notes": {
    "top": ["레몬", "베르가못"],
    "middle": ["생강", "자스민"],
    "base": ["샌달우드", "시더우드"]
  }
}
]

for item in seed_data:
    print(f"추가 중: {item['name']}")
    save_perfume(item)

print("✅ seed 데이터 삽입 완료")