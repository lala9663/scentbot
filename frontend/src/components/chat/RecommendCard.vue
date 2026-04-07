<template>
  <div class="recommend-card">
    <p class="message">{{ data.message }}</p>
    <div v-for="(item, i) in data.recommendations" :key="i" class="rec-item">
      <div class="rec-info">
        <span class="rec-name">{{ item.name }}</span>
        <span class="rec-brand">{{ item.brand }}</span>
      </div>
      <p class="rec-reason">{{ item.reason }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({ data: Object })
</script>

<style scoped>
.recommend-card {
  background: #fff;
  border: 0.5px solid #e0e0e0;
  border-radius: 16px;
  padding: 14px;
  max-width: 86%;
}
.message { font-size: 13px; color: #444; margin-bottom: 12px; line-height: 1.6; }
.rec-item {
  padding: 10px 12px;
  border: 0.5px solid #eee;
  border-radius: 10px;
  margin-bottom: 8px;
}
.rec-info { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; }
.rec-name { font-size: 13px; font-weight: 600; color: #111; }
.rec-brand { font-size: 11px; color: #aaa; }
.rec-reason { font-size: 12px; color: #777; line-height: 1.5; }
</style>
