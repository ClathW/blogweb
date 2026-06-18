<script setup>
import { ref, onMounted, watch } from 'vue'
import { getMyArticles, deleteArticle } from '@/api/articles'

const articles = ref([])
const loading = ref(false)
const page = ref(1)
const totalPages = ref(1)

async function fetchArticles() {
  loading.value = true
  try {
    const res = await getMyArticles({ page: page.value })
    articles.value = res.data.results
    totalPages.value = res.data.total_pages
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  if (!confirm('确定要删除这篇文章吗？')) return
  try {
    await deleteArticle(id)
    await fetchArticles()
  } catch (err) {
    alert(err.response?.data?.message || '删除失败')
  }
}

watch(page, fetchArticles)
onMounted(fetchArticles)
</script>

<template>
  <div class="my-articles">
    <div class="page-header">
      <h2>我的文章</h2>
      <router-link to="/editor" class="btn-primary">写新文章</router-link>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="articles.length === 0" class="empty">还没有发布文章</div>

    <div v-else>
      <table class="article-table">
        <thead>
          <tr>
            <th>标题</th>
            <th>状态</th>
            <th>分类</th>
            <th>阅读</th>
            <th>评论</th>
            <th>时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in articles" :key="item.id">
            <td>
              <router-link :to="`/articles/${item.id}`" class="title-link">{{ item.title }}</router-link>
            </td>
            <td>
              <span :class="`status status-${item.status}`">
                {{ item.status === 'published' ? '已发布' : item.status === 'draft' ? '草稿' : item.status }}
              </span>
            </td>
            <td>{{ item.category_name || '-' }}</td>
            <td>{{ item.view_count }}</td>
            <td>{{ item.comment_count }}</td>
            <td>{{ new Date(item.created_at).toLocaleDateString() }}</td>
            <td class="actions">
              <router-link :to="`/editor/${item.id}`" class="btn-edit">编辑</router-link>
              <button @click="handleDelete(item.id)" class="btn-delete">删除</button>
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
  </div>
</template>

<style scoped>
.my-articles { max-width: 980px; margin: 0 auto; }

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.page-header h2 { margin: 0; }

.btn-primary {
  padding: 0.55rem 1.25rem;
  background: var(--c-primary);
  color: #fff;
  border-radius: 6px;
  text-decoration: none;
  font-size: 0.9rem;
}

.loading, .empty { text-align: center; padding: 3rem 0; color: var(--c-text-muted); }

.article-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: var(--c-bg-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow);
}

.article-table th, .article-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--c-border);
  font-size: 0.9rem;
}

.article-table th {
  background: var(--c-table-head);
  color: var(--c-text-secondary);
  font-weight: 700;
}

.title-link { color: var(--c-text); text-decoration: none; font-weight: 600; }
.title-link:hover { color: var(--c-primary); }

.status { padding: 0.18rem 0.55rem; border-radius: 999px; font-size: 0.8rem; font-weight: 600; }
.status-published { background: var(--c-success-soft); color: var(--c-success); }
.status-draft { background: var(--c-warning-soft); color: var(--c-warning); }
.status-taken_down { background: var(--c-danger-soft); color: var(--c-danger); }
.status-archived { background: var(--c-primary-soft); color: var(--c-text-secondary); }

.actions { display: flex; gap: 0.5rem; }

.btn-edit {
  padding: 0.25rem 0.65rem;
  background: var(--c-primary);
  color: #fff;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.8rem;
}

.btn-delete {
  padding: 0.25rem 0.65rem;
  background: none;
  border: 1px solid rgba(220, 38, 38, 0.28);
  color: var(--c-danger);
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

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

@media (max-width: 760px) {
  .article-table {
    display: block;
    overflow-x: auto;
  }
}
</style>
