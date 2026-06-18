<script setup>
import NavBar from '@/components/layout/NavBar.vue'
</script>

<template>
  <NavBar />
  <main class="main-content">
    <router-view />
  </main>
</template>

<style>
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}
</style>
