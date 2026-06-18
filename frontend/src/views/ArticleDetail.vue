<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getArticle, deleteArticle } from '@/api/articles'
import { getComments, createComment, deleteComment } from '@/api/comments'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const article = ref(null)
const comments = ref([])
const loading = ref(true)
const newComment = ref('')
const submitting = ref(false)

// Delete confirmation
const showDeleteConfirm = ref(false)

async function fetchArticle() {
  loading.value = true
  try {
    const res = await getArticle(route.params.id)
    article.value = res.data
  } catch {
    article.value = null
  } finally {
    loading.value = false
  }
}

async function fetchComments() {
  try {
    const res = await getComments(route.params.id)
    comments.value = res.data
  } catch { /* ignore */ }
}

async function handlePostComment() {
  if (!newComment.value.trim()) return
  submitting.value = true
  try {
    await createComment(route.params.id, { content: newComment.value })
    newComment.value = ''
    await fetchComments()
  } catch (err) {
    alert(err.response?.data?.message || '评论发表失败')
  } finally {
    submitting.value = false
  }
}

async function handleDeleteComment(id) {
  if (!confirm('确定要删除此评论吗？')) return
  try {
    await deleteComment(id)
    await fetchComments()
  } catch (err) {
    alert(err.response?.data?.message || '删除失败')
  }
}

async function handleDeleteArticle() {
  try {
    await deleteArticle(route.params.id)
    router.push('/')
  } catch (err) {
    alert(err.response?.data?.message || '删除失败')
  }
}

onMounted(() => {
  fetchArticle()
  fetchComments()
})
</script>

<template>
  <div class="article-detail">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="!article" class="empty">文章不存在</div>
    <template v-else>
      <div class="article-header">
        <h1>{{ article.title }}</h1>
        <div class="article-meta">
          <span>作者：{{ article.author_name }}</span>
          <span v-if="article.category_name">分类：{{ article.category_name }}</span>
          <span>发布于 {{ new Date(article.created_at).toLocaleString() }}</span>
          <span>{{ article.view_count }} 阅读</span>
          <span>{{ article.comment_count }} 评论</span>
        </div>
        <div v-if="auth.user?.id === article.author || auth.isAdmin" class="article-actions">
          <router-link :to="`/editor/${article.id}`" class="btn-link">编辑</router-link>
          <button class="btn-danger" @click="showDeleteConfirm = true">删除</button>
        </div>
      </div>

      <div v-if="showDeleteConfirm" class="confirm-overlay">
        <div class="confirm-box">
          <p>确定要删除这篇文章吗？删除后无法恢复。</p>
          <div class="confirm-actions">
            <button @click="showDeleteConfirm = false">取消</button>
            <button class="btn-danger" @click="handleDeleteArticle">确认删除</button>
          </div>
        </div>
      </div>

      <div class="article-content" v-html="article.content"></div>

      <!-- Comments section -->
      <div class="comments-section">
        <h3>评论 ({{ comments.length }})</h3>

        <div v-if="auth.isLoggedIn" class="comment-form">
          <textarea
            v-model="newComment"
            placeholder="写下你的评论..."
            rows="3"
            maxlength="1000"
          ></textarea>
          <button :disabled="submitting || !newComment.trim()" @click="handlePostComment">
            {{ submitting ? '发表中...' : '发表评论' }}
          </button>
        </div>
        <p v-else class="login-hint">
          <router-link to="/login">登录</router-link>后即可评论
        </p>

        <div v-if="comments.length === 0" class="no-comments">暂无评论</div>
        <div v-for="comment in comments" :key="comment.id" class="comment">
          <div class="comment-header">
            <strong>{{ comment.author_name }}</strong>
            <span class="comment-time">{{ new Date(comment.created_at).toLocaleString() }}</span>
          </div>
          <p class="comment-content">{{ comment.content }}</p>
          <button
            v-if="auth.user?.id === comment.user || auth.isAdmin"
            class="comment-delete"
            @click="handleDeleteComment(comment.id)"
          >删除</button>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.article-detail {
  max-width: 800px;
  margin: 0 auto;
}

.loading, .empty { text-align: center; padding: 3rem 0; color: #9ca3af; }

.article-header {
  margin-bottom: 2rem;
}

.article-header h1 {
  font-size: 1.75rem;
  margin-bottom: 0.75rem;
}

.article-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #9ca3af;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.article-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-link {
  padding: 0.3rem 1rem;
  background: #2563eb;
  color: #fff;
  border-radius: 6px;
  text-decoration: none;
  font-size: 0.85rem;
}

.btn-danger {
  padding: 0.3rem 1rem;
  background: #dc2626;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
}

.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 200;
}

.confirm-box {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  max-width: 400px;
}

.confirm-box p {
  margin-bottom: 1.5rem;
}

.confirm-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.confirm-actions button {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
}

.article-content {
  font-size: 1.05rem;
  line-height: 1.8;
  color: #1f2937;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.comments-section {
  margin-top: 2rem;
}

.comments-section h3 {
  margin-bottom: 1rem;
}

.comment-form {
  margin-bottom: 1.5rem;
}

.comment-form textarea {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  resize: vertical;
  font-size: 0.9rem;
  box-sizing: border-box;
}

.comment-form textarea:focus {
  outline: none;
  border-color: #2563eb;
}

.comment-form button {
  margin-top: 0.5rem;
  padding: 0.5rem 1.5rem;
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.comment-form button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login-hint { color: #9ca3af; margin-bottom: 1.5rem; }
.no-comments { color: #9ca3af; text-align: center; padding: 2rem 0; }

.comment {
  border-bottom: 1px solid #f3f4f6;
  padding: 1rem 0;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.4rem;
}

.comment-header strong { font-size: 0.9rem; }
.comment-time { color: #9ca3af; font-size: 0.8rem; }

.comment-content {
  color: #4b5563;
  font-size: 0.9rem;
  line-height: 1.6;
}

.comment-delete {
  margin-top: 0.5rem;
  background: none;
  border: none;
  color: #dc2626;
  cursor: pointer;
  font-size: 0.8rem;
}
</style>
