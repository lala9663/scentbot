import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useCollectionStore = defineStore('collection', () => {
  const items = ref(JSON.parse(localStorage.getItem('scentai_collection') || '[]'))

  watch(items, (val) => {
    localStorage.setItem('scentai_collection', JSON.stringify(val))
  }, { deep: true })

  const add = (perfume) => {
    const exists = items.value.find(i => i.name === perfume.name && i.listType === perfume.listType)
    if (exists) return
    items.value.push({
      id: crypto.randomUUID(),
      name: perfume.name,
      brand: perfume.brand,
      perfumeType: perfume.perfumeType || perfume.type || 'EDP',
      ml: perfume.ml || null,
      notes: perfume.notes || { top: [], middle: [], base: [] },
      imageUrl: perfume.imageUrl || null,
      listType: perfume.listType || 'collection',
      createdAt: new Date().toISOString(),
    })
  }

  const remove = (id) => {
    items.value = items.value.filter(i => i.id !== id)
  }

  const collection = () => items.value.filter(i => i.listType === 'collection')
  const wishlist = () => items.value.filter(i => i.listType === 'wishlist')

  return { items, add, remove, collection, wishlist }
})
