<script setup>
import { ref, onMounted, watch } from 'vue'
import { getAdminUsers, updateUserStatus } from '@/api/admin'

const users = ref([])
const loading = ref(false)
const page = ref(1)
const totalPages = ref(1)
const keyword = ref('')
const statusFilter = ref('')

async function fetchUsers() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (keyword.value) params.keyword = keyword.value
    if (statusFilter.value) params.status = statusFilter.value
    const res = await getAdminUsers(params)
    users.value = res.data.results
    totalPages.value = res.data.total_pages
  } finally {
    loading.value = false
  }
}

async function toggleStatus(user) {
  const newStatus = user.status === 'active' ? 'disabled' : 'active'
  if (!confirm(`确定要${newStatus === 'active' ? '启用' : '禁用'}用户 ${user.username} 吗？`)) return
  try {
    await updateUserStatus(user.id, newStatus)
    await fetchUsers()
  } catch (err) {
    alert(err.response?.data?.message || '操作失败')
  }
}

watch(page, fetchUsers)
onMounted(fetchUsers)
</script>

<template>
  <div class="admin-users">
    <h2>用户管理</h2>

    <div class="filters">
      <input v-model="keyword" placeholder="搜索用户名或邮箱..." @keyup.enter="page=1;fetchUsers()" />
      <select v-model="statusFilter" @change="page=1;fetchUsers()">
        <option value="">全部状态</option>
        <option value="active">正常</option>
        <option value="disabled">已禁用</option>
      </select>
      <button @click="page=1;fetchUsers()">搜索</button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <table v-else class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>用户名</th>
          <th>邮箱</th>
          <th>角色</th>
          <th>状态</th>
          <th>注册时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role === 'admin' ? '管理员' : '普通用户' }}</td>
          <td>
            <span :class="`status-${user.status}`">
              {{ user.status === 'active' ? '正常' : '已禁用' }}
            </span>
          </td>
          <td>{{ new Date(user.date_joined).toLocaleDateString() }}</td>
          <td>
            <button @click="toggleStatus(user)">
              {{ user.status === 'active' ? '禁用' : '启用' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="totalPages > 1" class="pagination">
      <button :disabled="page <= 1" @click="page--">上一页</button>
      <span v-for="p in totalPages" :key="p">
        <button :class="{ current: p === page }" @click="page = p">{{ p }}</button>
      </span>
      <button :disabled="page >= totalPages" @click="page++">下一页</button>
    </div>
  </div>
</template>

<style scoped>
.admin-users { max-width: 1080px; margin: 0 auto; }

.admin-users h2 { margin-bottom: 1.5rem; }

.filters {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding: 0.9rem;
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  background: var(--c-bg-card);
  box-shadow: var(--shadow);
}

.filters input {
  flex: 1;
  padding: 0.5rem 0.8rem;
  border: 1px solid var(--c-border);
  border-radius: 6px;
  font-size: 0.9rem;
}

.filters select {
  padding: 0.5rem;
  border: 1px solid var(--c-border);
  border-radius: 6px;
}

.filters button {
  padding: 0.5rem 1rem;
  background: var(--c-primary);
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.loading { text-align: center; padding: 2rem; color: var(--c-text-muted); }

.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: var(--c-bg-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow);
}

.data-table th, .data-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--c-border);
  font-size: 0.9rem;
}

.data-table th {
  background: rgba(219, 234, 254, 0.5);
  color: var(--c-text-secondary);
  font-weight: 700;
}

.status-active { color: var(--c-success); font-weight: 700; }
.status-disabled { color: var(--c-danger); font-weight: 700; }

.data-table button {
  padding: 0.25rem 0.75rem;
  border: 1px solid var(--c-border);
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  font-size: 0.8rem;
}

.data-table button:hover { background: var(--c-primary-soft); }

.pagination {
  display: flex;
  justify-content: center;
  gap: 0.25rem;
  margin-top: 1.5rem;
}

.pagination button {
  padding: 0.4rem 0.7rem;
  border: 1px solid var(--c-border);
  border-radius: 6px;
  background: var(--c-bg-card);
  cursor: pointer;
}

.pagination button:disabled { opacity: 0.4; cursor: not-allowed; }
.pagination button.current { background: var(--c-primary); color: #fff; border-color: var(--c-primary); }

@media (max-width: 800px) {
  .filters { flex-direction: column; }
  .data-table { display: block; overflow-x: auto; }
}
</style>
