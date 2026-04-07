<template>
  <div class="calendar-view">
    <div class="topbar">
      <span class="logo">SCENTAI</span>
      <span class="month-label">{{ currentYear }}년 {{ currentMonth + 1 }}월</span>
    </div>

    <!-- 캘린더 -->
    <div class="cal-wrap">
      <div class="cal-nav">
        <button @click="prevMonth">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
        </button>
        <span class="cal-month">{{ currentYear }}년 {{ currentMonth + 1 }}월</span>
        <button @click="nextMonth">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#555" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
        </button>
      </div>

      <div class="legend">
        <span class="leg-item"><span class="dot am"></span>오전</span>
        <span class="leg-item"><span class="dot pm"></span>오후</span>
        <span class="leg-item"><span class="dot am"></span><span class="dot pm"></span>복수</span>
      </div>

      <div class="day-labels">
        <span v-for="d in ['일','월','화','수','목','금','토']" :key="d">{{ d }}</span>
      </div>

      <div class="cal-grid">
        <div v-for="(cell, i) in calendarCells" :key="i"
          class="cal-cell"
          :class="{ today: cell.isToday, selected: cell.date === selectedDate, empty: !cell.date }"
          @click="cell.date && selectDate(cell.date)"
        >
          <span class="num">{{ cell.day }}</span>
          <div class="dots">
            <span v-if="cell.dots?.am" class="dot am"></span>
            <span v-if="cell.dots?.pm" class="dot pm"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- 선택된 날짜 로그 -->
    <div class="log-section">
      <div class="log-date">{{ selectedDateLabel }}</div>

      <div v-if="selectedLogs.length === 0" class="no-log">기록된 향수가 없어요</div>

      <div v-for="log in selectedLogs" :key="log.id" class="log-item" :class="log.timeOfDay">
        <div class="log-thumbs">
          <div v-for="(p, idx) in log.perfumeDetails" :key="idx" class="log-thumb" :style="{ marginLeft: idx > 0 ? '-10px' : '0', zIndex: log.perfumeDetails.length - idx }">
            <img v-if="p?.imageUrl" :src="p.imageUrl" :alt="p.name" @error="p.imageUrl = null" />
            <svg v-else width="16" height="24" viewBox="0 0 48 72" fill="none">
              <rect x="19" y="2" width="10" height="7" rx="2" fill="#B5D4F4" stroke="#85B7EB" stroke-width="0.5"/>
              <rect x="21" y="8" width="6" height="5" rx="1" fill="#85B7EB"/>
              <path d="M10 18C10 14.5 14 13 24 13C34 13 38 14.5 38 18V60C38 63 36 66 24 66C12 66 10 63 10 60V18Z" fill="#E6F1FB" stroke="#85B7EB" stroke-width="0.5"/>
            </svg>
          </div>
        </div>
        <div class="log-info">
          <div class="log-time">{{ timeLabel(log.timeOfDay) }}</div>
          <div class="log-name">
            <span v-for="(p, idx) in log.perfumeDetails" :key="idx">
              <span v-if="idx > 0" class="slash"> / </span>{{ p?.name }}
            </span>
          </div>
          <div class="log-meta">{{ log.isLayering ? '레이어링' : '단독' }} · {{ log.perfumeDetails.map(p => p?.perfumeType).join(' + ') }}</div>
        </div>
        <button class="del-log" @click="calStore.removeLog(log.id)">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
      </div>

      <button class="add-log-btn" @click="openLogModal">+ 향수 기록 추가</button>
    </div>

    <!-- 기록 추가 모달 -->
    <div v-if="showModal" class="modal-bg" @click.self="showModal = false">
      <div class="modal">
        <div class="modal-handle"></div>
        <div class="modal-title">향수 기록 추가</div>
        <div class="field">
          <label>시간대</label>
          <div class="opt-row">
            <button v-for="t in timeopts" :key="t.value" :class="{ sel: logForm.timeOfDay === t.value, [t.value]: true }" @click="logForm.timeOfDay = t.value">{{ t.label }}</button>
          </div>
        </div>
        <div class="field">
          <label>향수 선택 <span class="hint">(복수 선택 시 레이어링)</span></label>
          <div v-if="colItems.length === 0" class="no-col">컬렉션에 향수를 먼저 추가해주세요</div>
          <div v-for="item in colItems" :key="item.id" class="sel-item" :class="{ selected: logForm.selectedIds.includes(item.id) }" @click="toggleSelect(item.id)">
            <div class="sel-thumb">
              <img v-if="item.imageUrl" :src="item.imageUrl" :alt="item.name" @error="item.imageUrl = null" />
              <svg v-else width="14" height="20" viewBox="0 0 48 72" fill="none">
                <rect x="19" y="2" width="10" height="7" rx="2" fill="#B5D4F4" stroke="#85B7EB" stroke-width="0.5"/>
                <path d="M10 18C10 14.5 14 13 24 13C34 13 38 14.5 38 18V60C38 63 36 66 24 66C12 66 10 63 10 60V18Z" fill="#E6F1FB" stroke="#85B7EB" stroke-width="0.5"/>
              </svg>
            </div>
            <span class="sel-name">{{ item.name }}</span>
            <div class="check" :class="{ on: logForm.selectedIds.includes(item.id) }">
              <svg v-if="logForm.selectedIds.includes(item.id)" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#185FA5" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>
            </div>
          </div>
        </div>

        <div v-if="logForm.selectedIds.length > 1" class="preview">
          <div class="preview-label">레이어링 미리보기</div>
          <div class="preview-names">
            <span v-for="(id, i) in logForm.selectedIds" :key="id">
              <span v-if="i > 0" class="slash"> / </span>{{ colItems.find(c => c.id === id)?.name }}
            </span>
          </div>
        </div>

        <button class="save-btn" @click="saveLog">기록 저장</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCalendarStore } from '../stores/calendar'
import { useCollectionStore } from '../stores/collection'

const calStore = useCalendarStore()
const colStore = useCollectionStore()

const today = new Date()
const currentYear = ref(today.getFullYear())
const currentMonth = ref(today.getMonth())
const selectedDate = ref(today.toISOString().slice(0, 10))

const colItems = computed(() => colStore.items.filter(i => i.listType === 'collection'))

const datesWithLogs = computed(() => calStore.getDatesWithLogs())

const calendarCells = computed(() => {
  const year = currentYear.value
  const month = currentMonth.value
  const firstDay = new Date(year, month, 1).getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const cells = []
  for (let i = 0; i < firstDay; i++) cells.push({ date: null, day: '' })
  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`
    const isToday = dateStr === today.toISOString().slice(0, 10)
    cells.push({ date: dateStr, day: d, isToday, dots: datesWithLogs.value[dateStr] })
  }
  return cells
})

const selectedLogs = computed(() => {
  return calStore.getLogsByDate(selectedDate.value).map(log => ({
    ...log,
    perfumeDetails: log.perfumes.map(id => colStore.items.find(i => i.id === id)).filter(Boolean)
  }))
})

const selectedDateLabel = computed(() => {
  if (!selectedDate.value) return ''
  const d = new Date(selectedDate.value)
  return `${d.getMonth() + 1}월 ${d.getDate()}일${selectedDate.value === today.toISOString().slice(0, 10) ? ' 오늘' : ''}`
})

const selectDate = (date) => { selectedDate.value = date }
const prevMonth = () => {
  if (currentMonth.value === 0) { currentYear.value--; currentMonth.value = 11 }
  else currentMonth.value--
}
const nextMonth = () => {
  if (currentMonth.value === 11) { currentYear.value++; currentMonth.value = 0 }
  else currentMonth.value++
}
const timeLabel = (t) => ({ morning: '오전', afternoon: '오후', allday: '하루종일' }[t] || t)

// 모달
const showModal = ref(false)
const timeopts = [{ value: 'morning', label: '오전' }, { value: 'afternoon', label: '오후' }, { value: 'allday', label: '하루종일' }]
const logForm = ref({ timeOfDay: 'morning', selectedIds: [] })

const openLogModal = () => {
  logForm.value = { timeOfDay: 'morning', selectedIds: [] }
  showModal.value = true
}
const toggleSelect = (id) => {
  const idx = logForm.value.selectedIds.indexOf(id)
  if (idx === -1) logForm.value.selectedIds.push(id)
  else logForm.value.selectedIds.splice(idx, 1)
}
const saveLog = () => {
  if (logForm.value.selectedIds.length === 0) return alert('향수를 선택해주세요')
  calStore.addLog({ date: selectedDate.value, timeOfDay: logForm.value.timeOfDay, perfumes: logForm.value.selectedIds })
  showModal.value = false
}
</script>

<style scoped>
.calendar-view { display: flex; flex-direction: column; min-height: 100%; }
.topbar { padding: 14px 18px; border-bottom: 0.5px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.logo { font-size: 15px; font-weight: 600; letter-spacing: 0.06em; }
.month-label { font-size: 12px; color: #aaa; }

.cal-wrap { padding: 12px 14px; border-bottom: 0.5px solid #eee; }
.cal-nav { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.cal-nav button { width: 28px; height: 28px; border-radius: 6px; border: 0.5px solid #eee; background: #f8f8f8; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.cal-month { font-size: 13px; font-weight: 600; color: #111; }

.legend { display: flex; gap: 12px; margin-bottom: 8px; }
.leg-item { display: flex; align-items: center; gap: 3px; font-size: 10.5px; color: #aaa; }

.day-labels { display: grid; grid-template-columns: repeat(7, 1fr); margin-bottom: 4px; }
.day-labels span { text-align: center; font-size: 10px; color: #aaa; padding: 3px 0; }

.cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; }
.cal-cell { aspect-ratio: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: 8px; cursor: pointer; }
.cal-cell.empty { cursor: default; }
.cal-cell.today { background: #E6F1FB; }
.cal-cell.selected { background: #185FA5; }
.cal-cell.selected .num { color: #fff; }
.num { font-size: 11px; color: #555; }
.cal-cell.today .num { color: #185FA5; font-weight: 600; }
.dots { display: flex; gap: 2px; margin-top: 2px; }
.cal-cell.selected .dots .dot { opacity: 0.7; }
.dot { width: 4px; height: 4px; border-radius: 50%; }
.dot.am { background: #185FA5; }
.dot.pm { background: #E24B4A; }

.log-section { padding: 14px; flex: 1; }
.log-date { font-size: 12px; color: #aaa; margin-bottom: 10px; }
.no-log { font-size: 13px; color: #ccc; text-align: center; padding: 20px 0; }

.log-item { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 12px; margin-bottom: 8px; border: 0.5px solid #eee; border-left-width: 2.5px; }
.log-item.morning { border-left-color: #185FA5; }
.log-item.afternoon { border-left-color: #E24B4A; }
.log-item.allday { border-left-color: #888; }
.log-thumbs { display: flex; align-items: center; flex-shrink: 0; }
.log-thumb { width: 34px; height: 42px; border-radius: 7px; background: #f0f4fb; border: 1px solid #fff; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.log-thumb img { width: 100%; height: 100%; object-fit: contain; }
.log-info { flex: 1; min-width: 0; }
.log-time { font-size: 10px; font-weight: 600; margin-bottom: 2px; }
.morning .log-time { color: #185FA5; }
.afternoon .log-time { color: #E24B4A; }
.allday .log-time { color: #888; }
.log-name { font-size: 12.5px; font-weight: 600; color: #111; }
.slash { color: #aaa; font-weight: 400; }
.log-meta { font-size: 10.5px; color: #aaa; margin-top: 2px; }
.del-log { background: none; border: none; cursor: pointer; padding: 4px; flex-shrink: 0; }

.add-log-btn { width: 100%; padding: 10px; border: 0.5px dashed #ddd; border-radius: 10px; font-size: 12px; color: #aaa; background: #fafafa; cursor: pointer; margin-top: 4px; }

.modal-bg { position: fixed; inset: 0; background: rgba(0,0,0,0.35); display: flex; align-items: flex-end; justify-content: center; z-index: 200; }
.modal { background: #fff; border-radius: 20px 20px 0 0; width: 100%; max-width: 430px; padding: 14px 16px 32px; max-height: 85dvh; overflow-y: auto; }
.modal-handle { width: 32px; height: 3px; background: #ddd; border-radius: 2px; margin: 0 auto 14px; }
.modal-title { font-size: 14px; font-weight: 600; margin-bottom: 14px; }

.field { margin-bottom: 12px; }
.field label { font-size: 11px; color: #888; display: block; margin-bottom: 5px; }
.hint { color: #bbb; font-size: 10px; }
.opt-row { display: flex; gap: 6px; }
.opt-row button { flex: 1; padding: 7px 0; font-size: 12px; border-radius: 8px; border: 0.5px solid #ddd; background: #f8f8f8; color: #888; cursor: pointer; }
.opt-row button.sel { font-weight: 600; }
.opt-row button.morning.sel { background: #E6F1FB; color: #185FA5; border-color: #85B7EB; }
.opt-row button.afternoon.sel { background: #FCEBEB; color: #A32D2D; border-color: #F09595; }
.opt-row button.allday.sel { background: #f0f0f0; color: #555; border-color: #ccc; }

.no-col { font-size: 12px; color: #bbb; padding: 12px 0; text-align: center; }
.sel-item { display: flex; align-items: center; gap: 8px; padding: 9px 10px; border: 0.5px solid #eee; border-radius: 10px; margin-bottom: 6px; cursor: pointer; }
.sel-item.selected { border-color: #85B7EB; background: #E6F1FB; }
.sel-thumb { width: 28px; height: 36px; border-radius: 6px; background: #f0f4fb; display: flex; align-items: center; justify-content: center; flex-shrink: 0; overflow: hidden; }
.sel-thumb img { width: 100%; height: 100%; object-fit: contain; }
.sel-name { flex: 1; font-size: 12.5px; color: #111; }
.check { width: 18px; height: 18px; border-radius: 5px; border: 0.5px solid #ddd; background: #f8f8f8; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.check.on { background: #E6F1FB; border-color: #85B7EB; }

.preview { background: #E6F1FB; border-radius: 8px; padding: 10px 12px; margin-bottom: 12px; border: 0.5px solid #B5D4F4; }
.preview-label { font-size: 10px; color: #185FA5; font-weight: 600; margin-bottom: 3px; }
.preview-names { font-size: 12.5px; color: #0C447C; font-weight: 600; }

.save-btn { width: 100%; padding: 11px; background: #185FA5; color: #fff; border: none; border-radius: 10px; font-size: 13px; font-weight: 600; cursor: pointer; }
</style>
