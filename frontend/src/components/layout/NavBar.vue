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
          <router-link v-if="auth.isAdmin" to="/manage" class="admin-link">管理</router-link>
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
  background: var(--c-nav-bg);
  border-bottom: 1px solid var(--c-border);
  padding: 0 1.25rem;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(18px);
  box-shadow: 0 1px 0 var(--c-card-shine);
}

.nav-container {
  max-width: 1180px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 68px;
  gap: 1rem;
}

.nav-brand {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--c-primary);
  letter-spacing: 0;
  white-space: nowrap;
}

.nav-links {
  display: flex;
  gap: 0.35rem;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.nav-links a {
  padding: 0.45rem 0.85rem;
  border-radius: 8px;
  color: var(--c-text-secondary);
  font-size: 0.9rem;
  transition: background 0.18s ease, color 0.18s ease, box-shadow 0.18s ease;
}

.nav-links a:hover {
  background: var(--c-primary-soft);
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
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.22);
}

.btn-write:hover {
  background: var(--c-primary-hover) !important;
  color: #fff !important;
}

.btn-register {
  background: var(--c-primary);
  color: #fff !important;
  font-weight: 500;
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.22);
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

@media (max-width: 720px) {
  .nav-container {
    align-items: flex-start;
    flex-direction: column;
    padding: 0.85rem 0;
  }

  .nav-links {
    justify-content: flex-start;
  }
}
</style>
