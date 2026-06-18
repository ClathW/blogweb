<script setup>
import { ref, onMounted, watch } from 'vue'
import { getAdminComments, adminDeleteComment } from '@/api/admin'

const comments = ref([])
const loading = ref(false)
const page = ref(1)
const totalPages = ref(1)
const keyword = ref('')
const articleId = ref('')

async function fetchComments() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (keyword.value) params.keyword = keyword.value
    if (articleId.value) params.article_id = articleId.value
    const res = await getAdminComments(params)
    comments.value = res.data.results
    totalPages.value = res.data.total_pages
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  if (!confirm('确定要强制删除此评论吗？')) return
  try {
    await adminDeleteComment(id)
    await fetchComments()
  } catch (err) {
    alert(err.response?.data?.message || '操作失败')
  }
}

watch(page, fetchComments)
onMounted(fetchComments)
</script>

<template>
  <div class="admin-comments">
    <h2>评论管理</h2>

    <div class="filters">
      <input v-model="keyword" placeholder="搜索评论内容..." @keyup.enter="page=1;fetchComments()" />
      <input v-model="articleId" placeholder="按文章ID筛选..." @keyup.enter="page=1;fetchComments()" />
      <button @click="page=1;fetchComments()">搜索</button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <table v-else class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>评论者</th>
          <th>文章</th>
          <th>内容</th>
          <th>时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in comments" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.author_name }}</td>
          <td>{{ item.article_title }}</td>
          <td class="content-cell">{{ item.content }}</td>
          <td>{{ new Date(item.created_at).toLocaleString() }}</td>
          <td>
            <button class="btn-danger" @click="handleDelete(item.id)">强制删除</button>
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
.admin-comments { max-width: 1080px; margin: 0 auto; }
.admin-comments h2 { margin-bottom: 1.5rem; }

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

.content-cell {
  max-width: 250px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-danger {
  padding: 0.25rem 0.75rem;
  border: 1px solid rgba(220, 38, 38, 0.28);
  color: var(--c-danger);
  background: #fff;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.btn-danger:hover { background: var(--c-danger-soft); }

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
