<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getArticle, deleteArticle } from '@/api/articles'
import { getComments, createComment, deleteComment } from '@/api/comments'
import { renderMarkdown } from '@/utils/markdown'

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

const renderedContent = computed(() => renderMarkdown(article.value?.content || ''))

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

      <div class="article-content markdown-body" v-html="renderedContent"></div>

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
  max-width: 860px;
  margin: 0 auto;
}

.loading, .empty { text-align: center; padding: 3rem 0; color: var(--c-text-muted); }

.article-header {
  margin-bottom: 2rem;
  padding: 1.75rem;
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  background: var(--c-bg-card);
  box-shadow: var(--shadow);
}

.article-header h1 {
  font-size: 2rem;
  line-height: 1.25;
  margin-bottom: 0.75rem;
}

.article-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--c-text-muted);
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.article-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-link {
  padding: 0.4rem 1rem;
  background: var(--c-primary);
  color: #fff;
  border-radius: 6px;
  text-decoration: none;
  font-size: 0.85rem;
}

.btn-danger {
  padding: 0.4rem 1rem;
  background: var(--c-danger);
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
}

.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(31, 41, 51, 0.36);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 200;
}

.confirm-box {
  background: var(--c-bg-soft);
  padding: 2rem;
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  max-width: 400px;
  box-shadow: var(--shadow-md);
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
  border: 1px solid var(--c-border);
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
}

.article-content {
  font-size: 1.05rem;
  line-height: 1.8;
  color: var(--c-text);
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--c-border);
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4) {
  margin: 1.35rem 0 0.65rem;
  line-height: 1.3;
}

.markdown-body :deep(h1) {
  font-size: 1.85rem;
}

.markdown-body :deep(h2) {
  font-size: 1.55rem;
}

.markdown-body :deep(h3) {
  font-size: 1.25rem;
}

.markdown-body :deep(p) {
  margin: 0.85rem 0;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 1.5rem;
  margin: 0.85rem 0;
}

.markdown-body :deep(li) {
  margin: 0.28rem 0;
}

.markdown-body :deep(blockquote) {
  margin: 1rem 0;
  padding: 0.2rem 1rem;
  border-left: 3px solid var(--c-primary);
  color: var(--c-text-secondary);
  background: var(--c-primary-soft);
  border-radius: 0 6px 6px 0;
}

.markdown-body :deep(code) {
  padding: 0.12rem 0.35rem;
  border-radius: 4px;
  background: var(--c-bg-soft);
  border: 1px solid var(--c-border);
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace;
  font-size: 0.92em;
}

.markdown-body :deep(pre) {
  overflow-x: auto;
  padding: 1rem;
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  background: #111827;
  color: #e5e7eb;
}

.markdown-body :deep(pre code) {
  padding: 0;
  border: none;
  background: transparent;
  color: inherit;
}

.markdown-body :deep(a) {
  overflow-wrap: anywhere;
}

.markdown-body :deep(img) {
  max-width: 100%;
  border-radius: var(--radius);
}

.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  display: block;
  overflow-x: auto;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid var(--c-border);
  padding: 0.55rem 0.7rem;
}

.markdown-body :deep(th) {
  background: var(--c-bg-soft);
}

.comments-section {
  margin-top: 2rem;
  padding: 1.5rem;
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  background: var(--c-bg-card);
}

.comments-section h3 {
  margin-bottom: 1rem;
}

.comment-form {
  margin-bottom: 1.5rem;
}

.comment-form textarea {
  width: 100%;
  padding: 0.7rem 0.8rem;
  border: 1px solid var(--c-border);
  border-radius: 6px;
  resize: vertical;
  font-size: 0.9rem;
  box-sizing: border-box;
}

.comment-form textarea:focus {
  outline: none;
  border-color: var(--c-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.comment-form button {
  margin-top: 0.5rem;
  padding: 0.5rem 1.5rem;
  background: var(--c-primary);
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.comment-form button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login-hint { color: var(--c-text-muted); margin-bottom: 1.5rem; }
.no-comments { color: var(--c-text-muted); text-align: center; padding: 2rem 0; }

.comment {
  border-bottom: 1px solid var(--c-border);
  padding: 1rem 0;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.4rem;
}

.comment-header strong { font-size: 0.9rem; }
.comment-time { color: var(--c-text-muted); font-size: 0.8rem; }

.comment-content {
  color: var(--c-text-secondary);
  font-size: 0.9rem;
  line-height: 1.6;
}

.comment-delete {
  margin-top: 0.5rem;
  background: none;
  border: none;
  color: var(--c-danger);
  cursor: pointer;
  font-size: 0.8rem;
}
</style>
