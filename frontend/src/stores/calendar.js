import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useCalendarStore = defineStore('calendar', () => {
  const logs = ref(JSON.parse(localStorage.getItem('scentai_logs') || '[]'))

  watch(logs, (val) => {
    localStorage.setItem('scentai_logs', JSON.stringify(val))
  }, { deep: true })

  const addLog = (log) => {
    logs.value.push({
      id: crypto.randomUUID(),
      date: log.date,
      timeOfDay: log.timeOfDay,
      perfumes: log.perfumes,
      isLayering: log.perfumes.length > 1,
      createdAt: new Date().toISOString(),
    })
  }

  const removeLog = (id) => {
    logs.value = logs.value.filter(l => l.id !== id)
  }

  const getLogsByDate = (date) => logs.value.filter(l => l.date === date)

  const getDatesWithLogs = () => {
    const map = {}
    logs.value.forEach(l => {
      if (!map[l.date]) map[l.date] = { am: false, pm: false }
      if (l.timeOfDay === 'morning' || l.timeOfDay === 'allday') map[l.date].am = true
      if (l.timeOfDay === 'afternoon' || l.timeOfDay === 'allday') map[l.date].pm = true
    })
    return map
  }

  return { logs, addLog, removeLog, getLogsByDate, getDatesWithLogs }
})
