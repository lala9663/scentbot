<template>
  <div class="chat-view">
    <div class="topbar">
      <span class="logo">SCENTAI</span>
      <button v-if="chatStore.messages.length > 0" class="clear-btn" @click="chatStore.clear()">초기화</button>
    </div>

    <div class="chat-area" ref="chatArea">
      <div v-if="chatStore.messages.length === 0" class="empty-state">
        <p>향수 이름이나 느낌으로 물어보세요</p>
        <div class="suggestions">
          <button v-for="s in suggestions" :key="s" @click="sendSuggestion(s)">{{ s }}</button>
        </div>
      </div>

      <div v-for="(msg, i) in chatStore.messages" :key="i" class="msg-row" :class="msg.role">
        <PerfumeCard v-if="msg.role === 'assistant' && msg.parsed?.type === 'perfume_info'" :data="msg.parsed" />
        <RecommendCard v-else-if="msg.role === 'assistant' && msg.parsed?.type === 'recommendation'" :data="msg.parsed" />
        <div v-else class="bubble" :class="msg.role">{{ msg.role === 'assistant' ? msg.parsed?.message || msg.content : msg.content }}</div>
      </div>

      <div v-if="chatStore.loading" class="msg-row assistant">
        <div class="bubble assistant loading">
          <span></span><span></span><span></span>
        </div>
      </div>
    </div>

    <div class="input-bar">
      <input
        v-model="input"
        @keyup.enter="send"
        placeholder="향수 이름이나 느낌으로 물어보세요..."
        :disabled="chatStore.loading"
      />
      <button @click="send" :disabled="chatStore.loading || !input.trim()">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="white"><path d="M2 21L23 12 2 3v7l15 2-15 2z"/></svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import axios from 'axios'
import PerfumeCard from '../components/chat/PerfumeCard.vue'
import RecommendCard from '../components/chat/RecommendCard.vue'
import { useChatStore } from '../stores/chat'
import { useCollectionStore } from '../stores/collection'

const input = ref('')
const chatArea = ref(null)
const chatStore = useChatStore()
const colStore = useCollectionStore()

const suggestions = [
  '블루 드 샤넬 알려줘',
  '내가 가진 향수 중에서 오늘 뭐 뿌릴까?',
  '데이트에 어울리는 향수 추천해줘',
]

const scrollToBottom = async () => {
  await nextTick()
  if (chatArea.value) chatArea.value.scrollTop = chatArea.value.scrollHeight
}

// 메시지 추가될 때마다 스크롤
watch(() => chatStore.messages.length, () => scrollToBottom())

const send = async () => {
  if (!input.value.trim() || chatStore.loading) return

  chatStore.addMessage({ role: 'user', content: input.value })
  input.value = ''
  chatStore.setLoading(true)

  try {
    const history = chatStore.messages
      .filter(m => m.role === 'user' || m.role === 'assistant')
      .map(m => ({ role: m.role, content: m.content }))

    const collection = colStore.items
      .filter(i => i.listType === 'collection')
      .map(i => ({ name: i.name, brand: i.brand, perfumeType: i.perfumeType, ml: i.ml }))

    const wishlist = colStore.items
      .filter(i => i.listType === 'wishlist')
      .map(i => ({ name: i.name, brand: i.brand, perfumeType: i.perfumeType }))

    const res = await axios.post('/api/chat', { messages: history, collection, wishlist })
    const raw = res.data.reply

    let parsed = null
    try { parsed = JSON.parse(raw) } catch {}

    chatStore.addMessage({ role: 'assistant', content: raw, parsed })
  } catch {
    chatStore.addMessage({
      role: 'assistant',
      content: null,
      parsed: { type: 'message', message: '오류가 발생했어요. 다시 시도해주세요.' }
    })
  } finally {
    chatStore.setLoading(false)
  }
}

const sendSuggestion = (text) => {
  input.value = text
  send()
}
</script>

<style scoped>
.chat-view { display: flex; flex-direction: column; height: 100%; }

.topbar {
  padding: 14px 18px;
  border-bottom: 0.5px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.logo { font-size: 15px; font-weight: 600; color: #111; letter-spacing: 0.06em; }
.clear-btn { font-size: 11px; color: #aaa; border: 0.5px solid #eee; background: none; padding: 4px 10px; border-radius: 6px; cursor: pointer; }

.chat-area {
  flex: 1;
  overflow-y: auto;
  padding: 16px 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.empty-state { margin: auto; text-align: center; color: #aaa; font-size: 14px; }
.suggestions { display: flex; flex-direction: column; gap: 8px; margin-top: 16px; }
.suggestions button {
  padding: 10px 16px; border-radius: 20px; border: 0.5px solid #ddd;
  background: #f8f8f8; font-size: 13px; color: #555; cursor: pointer;
}

.msg-row { display: flex; }
.msg-row.user { justify-content: flex-end; }
.msg-row.assistant { justify-content: flex-start; }

.bubble { max-width: 80%; padding: 10px 14px; border-radius: 16px; font-size: 13.5px; line-height: 1.6; }
.bubble.user { background: #185FA5; color: #fff; border-bottom-right-radius: 4px; }
.bubble.assistant { background: #f2f2f2; color: #111; border-bottom-left-radius: 4px; }

.bubble.loading { display: flex; gap: 4px; align-items: center; padding: 14px 18px; }
.bubble.loading span { width: 6px; height: 6px; border-radius: 50%; background: #aaa; animation: bounce 1s infinite; }
.bubble.loading span:nth-child(2) { animation-delay: 0.15s; }
.bubble.loading span:nth-child(3) { animation-delay: 0.3s; }
@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
}

.input-bar { padding: 10px 14px 14px; display: flex; gap: 8px; align-items: center; border-top: 0.5px solid #eee; }
.input-bar input { flex: 1; padding: 10px 14px; border-radius: 24px; border: 0.5px solid #ddd; background: #f8f8f8; font-size: 13.5px; outline: none; }
.input-bar button { width: 38px; height: 38px; border-radius: 50%; background: #185FA5; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.input-bar button:disabled { background: #ccc; cursor: not-allowed; }
</style>