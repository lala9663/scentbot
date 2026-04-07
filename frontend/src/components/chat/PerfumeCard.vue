<template>
  <div class="perfume-card">
    <div class="card-image">
      <img v-if="imgSrc" :src="imgSrc" :alt="data.name" @error="imgSrc = null" />
      <div v-else class="default-icon">
        <svg width="40" height="60" viewBox="0 0 48 72" fill="none">
          <rect x="19" y="2" width="10" height="7" rx="2" fill="#B5D4F4" stroke="#85B7EB" stroke-width="0.5"/>
          <rect x="21" y="8" width="6" height="5" rx="1" fill="#85B7EB"/>
          <path d="M10 18C10 14.5 14 13 24 13C34 13 38 14.5 38 18V60C38 63 36 66 24 66C12 66 10 63 10 60V18Z" fill="#E6F1FB" stroke="#85B7EB" stroke-width="0.5"/>
          <rect x="14" y="28" width="20" height="14" rx="2" fill="#B5D4F4" opacity="0.6"/>
        </svg>
      </div>
    </div>

    <div class="card-info">
      <div class="card-header">
        <span class="name">{{ data.name }}</span>
        <span class="type-badge">{{ data.perfumeType }}</span>
      </div>
      <div class="brand">{{ data.brand }}</div>

      <div class="notes">
        <div class="note-row">
          <span class="note-label">탑</span>
          <span v-for="n in data.notes.top" :key="n" class="tag top">{{ n }}</span>
        </div>
        <div class="note-row">
          <span class="note-label">미들</span>
          <span v-for="n in data.notes.middle" :key="n" class="tag mid">{{ n }}</span>
        </div>
        <div class="note-row">
          <span class="note-label">베이스</span>
          <span v-for="n in data.notes.base" :key="n" class="tag base">{{ n }}</span>
        </div>
      </div>

      <div class="meta-chips">
        <span v-for="s in data.season" :key="s" class="chip">{{ s }}</span>
        <span v-for="o in data.occasion" :key="o" class="chip">{{ o }}</span>
        <span class="chip">{{ data.mood }}</span>
      </div>

      <p class="description">{{ data.description }}</p>

      <div class="actions">
        <button class="btn-add" @click="addToCollection">+ 컬렉션 추가</button>
        <button class="btn-wish" @click="addToWishlist">+ 위시리스트</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCollectionStore } from '../../stores/collection'

const props = defineProps({ data: Object })
const store = useCollectionStore()

// GPT가 준 imageUrl 바로 사용, 없으면 null (기본 아이콘 표시)
const imgSrc = ref(props.data.imageUrl || null)

const addToCollection = () => {
  store.add({ ...props.data, listType: 'collection' })
  alert('컬렉션에 추가됐어요!')
}
const addToWishlist = () => {
  store.add({ ...props.data, listType: 'wishlist' })
  alert('위시리스트에 추가됐어요!')
}
</script>

<style scoped>
.perfume-card {
  background: #fff;
  border: 0.5px solid #e0e0e0;
  border-radius: 16px;
  overflow: hidden;
  max-width: 86%;
}
.card-image {
  width: 100%;
  height: 120px;
  background: #f0f4fb;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 0.5px solid #eee;
}
.card-image img { width: 100%; height: 100%; object-fit: contain; padding: 8px; }
.card-info { padding: 12px 14px; }
.card-header { display: flex; align-items: center; gap: 8px; margin-bottom: 2px; }
.name { font-size: 14px; font-weight: 600; color: #111; }
.type-badge { font-size: 10px; padding: 2px 6px; border-radius: 4px; background: #eee; color: #555; }
.brand { font-size: 11px; color: #999; margin-bottom: 10px; }

.notes { display: flex; flex-direction: column; gap: 6px; margin-bottom: 10px; }
.note-row { display: flex; align-items: center; gap: 5px; flex-wrap: wrap; }
.note-label { font-size: 10px; color: #aaa; width: 26px; flex-shrink: 0; }
.tag { padding: 3px 8px; border-radius: 20px; font-size: 11px; font-weight: 500; }
.top { background: #E6F1FB; color: #0C447C; }
.mid { background: #EEEDFE; color: #3C3489; }
.base { background: #E1F5EE; color: #085041; }

.meta-chips { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 10px; }
.chip { padding: 3px 8px; border-radius: 5px; font-size: 11px; background: #f5f5f5; color: #666; border: 0.5px solid #e8e8e8; }

.description { font-size: 12px; color: #777; line-height: 1.5; margin-bottom: 12px; }

.actions { display: flex; gap: 6px; }
.btn-add, .btn-wish {
  flex: 1; padding: 7px; border-radius: 8px; font-size: 11.5px; cursor: pointer;
}
.btn-add { background: #185FA5; color: #fff; border: none; }
.btn-wish { background: #fff; color: #185FA5; border: 0.5px solid #185FA5; }
</style>
