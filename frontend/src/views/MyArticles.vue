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
.my-articles { max-width: 900px; margin: 0 auto; }

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.page-header h2 { margin: 0; }

.btn-primary {
  padding: 0.5rem 1.25rem;
  background: #2563eb;
  color: #fff;
  border-radius: 6px;
  text-decoration: none;
  font-size: 0.9rem;
}

.loading, .empty { text-align: center; padding: 3rem 0; color: #9ca3af; }

.article-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

.article-table th, .article-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #f3f4f6;
  font-size: 0.9rem;
}

.article-table th {
  background: #f9fafb;
  color: #6b7280;
  font-weight: 500;
}

.title-link { color: #111827; text-decoration: none; }
.title-link:hover { color: #2563eb; }

.status { padding: 0.15rem 0.5rem; border-radius: 10px; font-size: 0.8rem; }
.status-published { background: #dcfce7; color: #16a34a; }
.status-draft { background: #fef3c7; color: #d97706; }
.status-taken_down { background: #fee2e2; color: #dc2626; }
.status-archived { background: #f3f4f6; color: #6b7280; }

.actions { display: flex; gap: 0.5rem; }

.btn-edit {
  padding: 0.2rem 0.6rem;
  background: #2563eb;
  color: #fff;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.8rem;
}

.btn-delete {
  padding: 0.2rem 0.6rem;
  background: none;
  border: 1px solid #fca5a5;
  color: #dc2626;
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
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
}

.pagination button:disabled { opacity: 0.4; cursor: not-allowed; }
.pagination button.current { background: #2563eb; color: #fff; border-color: #2563eb; }
</style>
