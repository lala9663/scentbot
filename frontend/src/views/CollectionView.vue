<template>
  <div class="collection-view">
    <div class="topbar">
      <span class="logo">SCENTAI</span>
      <span class="count">{{ activeItems.length }}개</span>
    </div>

    <div class="seg-tabs">
      <button :class="{ active: tab === 'collection' }" @click="tab = 'collection'">내 컬렉션</button>
      <button :class="{ active: tab === 'wishlist' }" @click="tab = 'wishlist'">위시리스트</button>
    </div>

    <div class="list">
      <div class="list-header">
        <span class="list-count">{{ tab === 'collection' ? '보유 향수' : '갖고 싶은 향수' }} {{ activeItems.length }}개</span>
        <button class="add-btn" @click="openModal(null)">+ 추가</button>
      </div>

      <div v-if="activeItems.length === 0" class="empty">
        <p>아직 추가된 향수가 없어요</p>
      </div>

      <div v-for="item in activeItems" :key="item.id" class="item-card">
        <div class="item-thumb">
          <img v-if="item.imageUrl" :src="item.imageUrl" :alt="item.name" @error="item.imageUrl = null" />
          <div v-else class="default-icon">
            <svg width="24" height="36" viewBox="0 0 48 72" fill="none">
              <rect x="19" y="2" width="10" height="7" rx="2" fill="#B5D4F4" stroke="#85B7EB" stroke-width="0.5"/>
              <rect x="21" y="8" width="6" height="5" rx="1" fill="#85B7EB"/>
              <path d="M10 18C10 14.5 14 13 24 13C34 13 38 14.5 38 18V60C38 63 36 66 24 66C12 66 10 63 10 60V18Z" fill="#E6F1FB" stroke="#85B7EB" stroke-width="0.5"/>
            </svg>
          </div>
        </div>
        <div class="item-info">
          <div class="item-name">{{ item.name }}</div>
          <div class="item-meta">
            <span class="brand">{{ item.brand }}</span>
            <span class="badge type">{{ item.perfumeType }}</span>
            <span v-if="item.ml" class="badge ml">{{ item.ml }}ml</span>
            <span v-if="tab === 'wishlist'" class="badge wish">위시</span>
          </div>
          <div class="item-tags">
            <span v-for="n in item.notes?.top?.slice(0,2)" :key="n" class="tag top">{{ n }}</span>
            <span v-for="n in item.notes?.middle?.slice(0,1)" :key="n" class="tag mid">{{ n }}</span>
            <span v-for="n in item.notes?.base?.slice(0,1)" :key="n" class="tag base">{{ n }}</span>
          </div>
        </div>
        <button class="delete-btn" @click="remove(item.id)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5">
            <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4h6v2"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- 등록 모달 -->
    <div v-if="showModal" class="modal-bg" @click.self="showModal = false">
      <div class="modal">
        <div class="modal-handle"></div>
        <div class="modal-title">향수 추가</div>

        <div class="field">
          <label>목록</label>
          <div class="opt-row">
            <button :class="{ sel: form.listType === 'collection' }" @click="form.listType = 'collection'">내 컬렉션</button>
            <button :class="{ sel: form.listType === 'wishlist' }" @click="form.listType = 'wishlist'">위시리스트</button>
          </div>
        </div>

        <div class="field">
          <label>바틀 이미지</label>
          <div class="img-opts">
            <div :class="['img-opt', { sel: form.imageType === 'upload' }]" @click="form.imageType = 'upload'">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
              <span>직접 업로드</span>
              <input v-if="form.imageType === 'upload'" type="file" accept="image/*" @change="onFileChange" class="file-input" />
            </div>
            <div :class="['img-opt', { sel: form.imageType === 'auto' }]" @click="form.imageType = 'auto'">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10A15.3 15.3 0 0 1 8 12a15.3 15.3 0 0 1 4-10z"/></svg>
              <span>대표 이미지</span>
            </div>
            <div :class="['img-opt', { sel: form.imageType === 'none' }]" @click="form.imageType = 'none'">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
              <span>기본 아이콘</span>
            </div>
          </div>
        </div>

        <div class="row2">
          <div class="field">
            <label>향수 이름</label>
            <input v-model="form.name" placeholder="Bleu de Chanel" />
          </div>
          <div class="field">
            <label>브랜드</label>
            <input v-model="form.brand" placeholder="Chanel" />
          </div>
        </div>

        <div class="row2">
          <div class="field">
            <label>타입</label>
            <div class="opt-row">
              <button v-for="t in types" :key="t" :class="{ sel: form.perfumeType === t }" @click="form.perfumeType = t">{{ t }}</button>
            </div>
          </div>
          <div class="field" v-if="form.listType === 'collection'">
            <label>용량</label>
            <div class="opt-row">
              <button v-for="m in mls" :key="m" :class="{ sel: form.ml === m }" @click="selectMl(m)">{{ m }}</button>
              <input v-if="form.ml === 'custom'" v-model="form.mlCustom" placeholder="ml" class="ml-input" type="number" />
            </div>
          </div>
        </div>

        <button class="save-btn" @click="save">저장하기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCollectionStore } from '../stores/collection'

const store = useCollectionStore()
const tab = ref('collection')
const showModal = ref(false)
const types = ['EDC', 'EDT', 'EDP', 'Parfum']
const mls = [30, 50, 100, 'custom']

const form = ref({
  listType: 'collection',
  imageType: 'auto',
  imageUrl: null,
  name: '',
  brand: '',
  perfumeType: 'EDP',
  ml: null,
  mlCustom: '',
})

const activeItems = computed(() =>
  store.items.filter(i => i.listType === tab.value)
)

const openModal = () => {
  form.value = { listType: tab.value, imageType: 'auto', imageUrl: null, name: '', brand: '', perfumeType: 'EDP', ml: null, mlCustom: '' }
  showModal.value = true
}

const selectMl = (m) => { form.value.ml = m }

const onFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (ev) => { form.value.imageUrl = ev.target.result }
  reader.readAsDataURL(file)
}

const save = () => {
  if (!form.value.name.trim()) return alert('향수 이름을 입력해주세요')
  const ml = form.value.ml === 'custom' ? Number(form.value.mlCustom) : form.value.ml
  store.add({
    ...form.value,
    ml,
    imageUrl: form.value.imageType === 'none' ? null : form.value.imageUrl,
    notes: { top: [], middle: [], base: [] },
  })
  showModal.value = false
}

const remove = (id) => {
  if (confirm('삭제할까요?')) store.remove(id)
}
</script>

<style scoped>
.collection-view { display: flex; flex-direction: column; min-height: 100%; }
.topbar { padding: 14px 18px; border-bottom: 0.5px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.logo { font-size: 15px; font-weight: 600; letter-spacing: 0.06em; }
.count { font-size: 12px; color: #aaa; }

.seg-tabs { display: flex; margin: 12px 14px 0; border: 0.5px solid #ddd; border-radius: 8px; overflow: hidden; }
.seg-tabs button { flex: 1; padding: 8px 0; font-size: 12px; color: #888; background: #f8f8f8; border: none; cursor: pointer; }
.seg-tabs button.active { background: #fff; color: #185FA5; font-weight: 600; }

.list { padding: 12px 14px; }
.list-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.list-count { font-size: 12px; color: #aaa; }
.add-btn { font-size: 11px; color: #185FA5; border: 0.5px solid #85B7EB; padding: 5px 12px; border-radius: 6px; background: #E6F1FB; cursor: pointer; }

.empty { padding: 40px; text-align: center; color: #bbb; font-size: 13px; }

.item-card { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border: 0.5px solid #eee; border-radius: 12px; margin-bottom: 8px; }
.item-thumb { width: 42px; height: 52px; border-radius: 8px; background: #f0f4fb; border: 0.5px solid #eee; display: flex; align-items: center; justify-content: center; flex-shrink: 0; overflow: hidden; }
.item-thumb img { width: 100%; height: 100%; object-fit: contain; }
.item-info { flex: 1; min-width: 0; }
.item-name { font-size: 13px; font-weight: 600; color: #111; }
.item-meta { display: flex; align-items: center; gap: 4px; margin-top: 3px; flex-wrap: wrap; }
.brand { font-size: 10.5px; color: #aaa; }
.badge { font-size: 10px; padding: 1px 6px; border-radius: 4px; }
.type { background: #eee; color: #555; }
.ml { background: #EEEDFE; color: #3C3489; }
.wish { background: #FAEEDA; color: #633806; }
.item-tags { display: flex; gap: 4px; margin-top: 5px; flex-wrap: wrap; }
.tag { padding: 2px 7px; border-radius: 20px; font-size: 10.5px; font-weight: 500; }
.top { background: #E6F1FB; color: #0C447C; }
.mid { background: #EEEDFE; color: #3C3489; }
.base { background: #E1F5EE; color: #085041; }
.delete-btn { background: none; border: none; cursor: pointer; padding: 4px; flex-shrink: 0; }

.modal-bg { position: fixed; inset: 0; background: rgba(0,0,0,0.35); display: flex; align-items: flex-end; justify-content: center; z-index: 200; }
.modal { background: #fff; border-radius: 20px 20px 0 0; width: 100%; max-width: 430px; padding: 14px 16px 32px; max-height: 90dvh; overflow-y: auto; }
.modal-handle { width: 32px; height: 3px; background: #ddd; border-radius: 2px; margin: 0 auto 14px; }
.modal-title { font-size: 14px; font-weight: 600; color: #111; margin-bottom: 14px; }

.field { margin-bottom: 12px; }
.field label { font-size: 11px; color: #888; display: block; margin-bottom: 5px; }
.field input { width: 100%; padding: 8px 11px; border-radius: 8px; border: 0.5px solid #ddd; font-size: 13px; outline: none; }
.row2 { display: flex; gap: 10px; }
.row2 .field { flex: 1; }

.opt-row { display: flex; gap: 5px; flex-wrap: wrap; }
.opt-row button { flex: 1; padding: 6px 0; font-size: 11px; border-radius: 6px; border: 0.5px solid #ddd; color: #888; background: #f8f8f8; cursor: pointer; min-width: 40px; }
.opt-row button.sel { background: #E6F1FB; color: #185FA5; border-color: #85B7EB; font-weight: 600; }

.img-opts { display: flex; gap: 6px; }
.img-opt { flex: 1; border: 0.5px solid #ddd; border-radius: 8px; padding: 10px 6px; text-align: center; cursor: pointer; background: #f8f8f8; position: relative; }
.img-opt.sel { border-color: #85B7EB; background: #E6F1FB; }
.img-opt svg { display: block; margin: 0 auto 4px; color: #aaa; }
.img-opt.sel svg { color: #185FA5; }
.img-opt span { font-size: 10px; color: #888; line-height: 1.4; }
.img-opt.sel span { color: #0C447C; }
.file-input { position: absolute; inset: 0; opacity: 0; cursor: pointer; }

.ml-input { width: 60px; padding: 5px 8px; border-radius: 6px; border: 0.5px solid #ddd; font-size: 12px; }

.save-btn { width: 100%; padding: 11px; background: #185FA5; color: #fff; border: none; border-radius: 10px; font-size: 13px; font-weight: 600; cursor: pointer; margin-top: 4px; }
</style>
