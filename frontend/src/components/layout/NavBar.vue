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
          <router-link to="/editor" class="btn-write">写文章</router-link>
          <router-link to="/my-articles">我的</router-link>
          <router-link to="/profile" class="user-link">
            {{ auth.user?.username }}
          </router-link>
          <router-link v-if="auth.isAdmin" to="/admin" class="admin-link">后台</router-link>
          <a href="#" @click.prevent="handleLogout" class="logout-link">退出</a>
        </template>
        <template v-else>
          <router-link to="/login">登录</router-link>
          <router-link to="/register" class="btn-register">注册</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background: var(--c-bg-card);
  border-bottom: 1px solid var(--c-border);
  padding: 0 1.5rem;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(8px);
}

.nav-container {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.nav-brand {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--c-primary);
  letter-spacing: -0.02em;
}

.nav-links {
  display: flex;
  gap: 0.25rem;
  align-items: center;
}

.nav-links a {
  padding: 0.4rem 0.85rem;
  border-radius: 8px;
  color: var(--c-text-secondary);
  font-size: 0.9rem;
  transition: all 0.15s;
}

.nav-links a:hover {
  background: var(--c-primary-light);
  color: var(--c-primary);
}

.nav-links a.router-link-active {
  color: var(--c-primary);
  font-weight: 600;
}

.btn-write {
  background: var(--c-primary) !important;
  color: #fff !important;
  font-weight: 500;
}

.btn-write:hover {
  background: var(--c-primary-hover) !important;
  color: #fff !important;
}

.btn-register {
  background: var(--c-primary);
  color: #fff !important;
  font-weight: 500;
}

.btn-register:hover {
  background: var(--c-primary-hover);
}

.user-link {
  font-weight: 500;
  color: var(--c-text) !important;
}

.admin-link {
  color: var(--c-warning) !important;
  font-weight: 500;
}

.logout-link {
  color: var(--c-text-muted) !important;
  font-size: 0.85rem !important;
}
</style>
