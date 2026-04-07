<template>
  <div class="app-wrapper">
    <main class="main-content">
      <RouterView />
    </main>
    <BottomNav />
  </div>
</template>

<script setup>
import BottomNav from './components/BottomNav.vue'
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #f5f5f5;
  display: flex;
  justify-content: center;
}

.app-wrapper {
  width: 100%;
  max-width: 430px;
  min-height: 100dvh;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  position: relative;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 64px;
}
</style>
