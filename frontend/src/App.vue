<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import NavBar from '@/components/layout/NavBar.vue'

const auth = useAuthStore()
const router = useRouter()

onMounted(async () => {
  await auth.checkAuth()
})

// Route guards
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresAdmin && !auth.isAdmin) {
    next({ name: 'home' })
  } else if (to.meta.guest && auth.isLoggedIn) {
    next({ name: 'home' })
  } else {
    next()
  }
})
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
