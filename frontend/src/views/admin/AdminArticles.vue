<script setup>
import { ref, onMounted, watch } from 'vue'
import { getAdminArticles, adminDeleteArticle } from '@/api/admin'
import { getCategories } from '@/api/articles'

const articles = ref([])
const categories = ref([])
const loading = ref(false)
const page = ref(1)
const totalPages = ref(1)
const keyword = ref('')
const categoryFilter = ref('')

async function fetchArticles() {
  loading.value = true
  try {
    const params = { page: page.value }
    if (keyword.value) params.keyword = keyword.value
    if (categoryFilter.value) params.category = categoryFilter.value
    const res = await getAdminArticles(params)
    articles.value = res.data.results
    totalPages.value = res.data.total_pages
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  if (!confirm('确定要强制删除此文章吗？此操作不可恢复。')) return
  try {
    await adminDeleteArticle(id)
    await fetchArticles()
  } catch (err) {
    alert(err.response?.data?.message || '操作失败')
  }
}

async function fetchCategories() {
  try {
    const res = await getCategories()
    categories.value = res.data
  } catch { /* ignore */ }
}

watch(page, fetchArticles)
onMounted(() => {
  fetchCategories()
  fetchArticles()
})
</script>

<template>
  <div class="admin-articles">
    <h2>文章管理</h2>

    <div class="filters">
      <input v-model="keyword" placeholder="搜索标题或内容..." @keyup.enter="page=1;fetchArticles()" />
      <select v-model="categoryFilter" @change="page=1;fetchArticles()">
        <option value="">全部分类</option>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
      </select>
      <button @click="page=1;fetchArticles()">搜索</button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <table v-else class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>标题</th>
          <th>作者</th>
          <th>分类</th>
          <th>状态</th>
          <th>阅读</th>
          <th>时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in articles" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.title }}</td>
          <td>{{ item.author_name }}</td>
          <td>{{ item.category_name || '-' }}</td>
          <td>
            <span :class="`status-${item.status}`">
              {{ item.status === 'published' ? '已发布' : item.status }}
            </span>
          </td>
          <td>{{ item.view_count }}</td>
          <td>{{ new Date(item.created_at).toLocaleDateString() }}</td>
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
.admin-articles { max-width: 1080px; margin: 0 auto; }
.admin-articles h2 { margin-bottom: 1.5rem; }

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
  background: var(--c-table-head);
  color: var(--c-text-secondary);
  font-weight: 700;
}

.status-published { color: var(--c-success); font-weight: 700; }
.status-draft { color: var(--c-warning); font-weight: 700; }
.status-taken_down { color: var(--c-danger); font-weight: 700; }
.status-archived { color: var(--c-text-secondary); font-weight: 700; }

.btn-danger {
  padding: 0.25rem 0.75rem;
  border: 1px solid rgba(220, 38, 38, 0.28);
  color: var(--c-danger);
  background: var(--c-control-bg);
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
