<script setup>
import { ref, onMounted, watch } from 'vue'
import { getArticles, getCategories } from '@/api/articles'

const articles = ref([])
const categories = ref([])
const loading = ref(false)
const page = ref(1)
const totalPages = ref(1)
const selectedCategory = ref('')

async function fetchArticles() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: 10 }
    if (selectedCategory.value) params.category = selectedCategory.value
    const res = await getArticles(params)
    articles.value = res.data.results
    totalPages.value = res.data.total_pages
    page.value = res.data.page
  } finally {
    loading.value = false
  }
}

async function fetchCategories() {
  try {
    const res = await getCategories()
    categories.value = res.data
  } catch { /* ignore */ }
}

function changePage(p) {
  page.value = p
}

function filterByCategory(id) {
  selectedCategory.value = id
  page.value = 1
}

watch(page, fetchArticles)
watch(selectedCategory, () => { page.value = 1; fetchArticles() })

onMounted(() => {
  fetchCategories()
  fetchArticles()
})
</script>

<template>
  <div class="home-page">
    <div class="page-header">
      <h1>博客文章</h1>
      <div class="category-filter">
        <button
          :class="{ active: !selectedCategory }"
          @click="filterByCategory('')"
        >全部</button>
        <button
          v-for="cat in categories"
          :key="cat.id"
          :class="{ active: selectedCategory === String(cat.id) }"
          @click="filterByCategory(String(cat.id))"
        >{{ cat.name }}</button>
      </div>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="articles.length === 0" class="empty">
      暂无文章
    </div>

    <div v-else class="article-list">
      <article v-for="item in articles" :key="item.id" class="article-card">
        <router-link :to="`/articles/${item.id}`" class="article-title">
          {{ item.title }}
        </router-link>
        <p class="article-summary">{{ item.summary || item.content?.slice(0, 200) }}</p>
        <div class="article-meta">
          <span>作者：{{ item.author_name }}</span>
          <span v-if="item.category_name">分类：{{ item.category_name }}</span>
          <span>{{ new Date(item.created_at).toLocaleDateString() }}</span>
          <span>{{ item.view_count }} 阅读</span>
          <span>{{ item.comment_count }} 评论</span>
        </div>
      </article>

      <div v-if="totalPages > 1" class="pagination">
        <button :disabled="page <= 1" @click="changePage(page - 1)">上一页</button>
        <span v-for="p in totalPages" :key="p">
          <button
            :class="{ current: p === page }"
            @click="changePage(p)"
          >{{ p }}</button>
        </span>
        <button :disabled="page >= totalPages" @click="changePage(page + 1)">下一页</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.page-header h1 { margin: 0; }

.category-filter {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.category-filter button {
  padding: 0.3rem 0.8rem;
  border: 1px solid #d1d5db;
  border-radius: 20px;
  background: #fff;
  cursor: pointer;
  font-size: 0.85rem;
  color: #6b7280;
}

.category-filter button.active {
  background: #2563eb;
  color: #fff;
  border-color: #2563eb;
}

.loading, .empty {
  text-align: center;
  color: #9ca3af;
  padding: 3rem 0;
}

.article-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
}

.article-title {
  font-size: 1.15rem;
  font-weight: 600;
  color: #111827;
  text-decoration: none;
  display: block;
  margin-bottom: 0.5rem;
}

.article-title:hover { color: #2563eb; }

.article-summary {
  color: #6b7280;
  font-size: 0.9rem;
  line-height: 1.6;
  margin-bottom: 0.75rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #9ca3af;
  flex-wrap: wrap;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.25rem;
  margin-top: 1.5rem;
}

.pagination button {
  padding: 0.4rem 0.7rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
  font-size: 0.85rem;
}

.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.pagination button.current {
  background: #2563eb;
  color: #fff;
  border-color: #2563eb;
}
</style>
