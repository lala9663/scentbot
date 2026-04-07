import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
  const messages = ref([])
  const loading = ref(false)

  const addMessage = (msg) => {
    messages.value.push(msg)
  }

  const setLoading = (val) => {
    loading.value = val
  }

  const clear = () => {
    messages.value = []
  }

  return { messages, loading, addMessage, setLoading, clear }
})