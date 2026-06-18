<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

async function handleLogout() {
  await auth.logoutUser()
  router.push('/')
}
</script>

<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="nav-brand">BlogWeb</router-link>
      <div class="nav-links">
        <router-link to="/">首页</router-link>
        <template v-if="auth.isLoggedIn">
          <router-link to="/editor">写文章</router-link>
          <router-link to="/my-articles">我的文章</router-link>
          <router-link to="/profile">个人中心</router-link>
          <router-link v-if="auth.isAdmin" to="/admin">后台管理</router-link>
          <a href="#" @click.prevent="handleLogout">退出</a>
        </template>
        <template v-else>
          <router-link to="/login">登录</router-link>
          <router-link to="/register">注册</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  padding: 0 1rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
}

.nav-brand {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2563eb;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.25rem;
  align-items: center;
}

.nav-links a {
  color: #374151;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: #2563eb;
}
</style>
