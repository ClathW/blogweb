<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createArticle, updateArticle, getArticle, getCategories } from '@/api/articles'
import { renderMarkdown } from '@/utils/markdown'

const route = useRoute()
const router = useRouter()

const isEdit = ref(false)
const categories = ref([])
const loading = ref(false)
const form = ref({
  title: '',
  content: '',
  category: '',
})

const error = ref('')
const activePane = ref('edit')
const renderedPreview = computed(() => renderMarkdown(form.value.content || ''))

async function fetchCategories() {
  try {
    const res = await getCategories()
    categories.value = res.data
  } catch { /* ignore */ }
}

async function fetchArticle() {
  const id = route.params.id
  if (!id) return
  isEdit.value = true
  try {
    const res = await getArticle(id)
    const article = res.data
    form.value.title = article.title
    form.value.content = article.content
    form.value.category = article.category_id || ''
  } catch {
    error.value = '文章不存在'
  }
}

async function handleSubmit() {
  error.value = ''

  if (!form.value.title || form.value.title.length > 100) {
    error.value = '标题长度为1-100个字符'
    return
  }
  if (!form.value.content || form.value.content.length > 50000) {
    error.value = '正文长度为1-50000个字符'
    return
  }

  loading.value = true
  try {
    const data = { ...form.value }
    if (!data.category) data.category = null
    else data.category = Number(data.category)

    if (isEdit.value) {
      await updateArticle(route.params.id, data)
    } else {
      await createArticle(data)
    }
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.message || '操作失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCategories()
  fetchArticle()
})
</script>

<template>
  <div class="editor-page">
    <h2>{{ isEdit ? '编辑文章' : '写文章' }}</h2>

    <form @submit.prevent="handleSubmit">
      <div v-if="error" class="error-msg">{{ error }}</div>

      <div class="form-group">
        <label>标题 <span class="required">*</span></label>
        <input v-model="form.title" type="text" placeholder="文章标题（1-100字）" maxlength="100" />
      </div>

      <div class="form-group">
        <label>分类</label>
        <select v-model="form.category">
          <option value="">请选择分类</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
        </select>
      </div>

      <div class="form-group markdown-field">
        <div class="field-header">
          <label>正文 <span class="required">*</span></label>
          <div class="editor-tabs" aria-label="Markdown编辑模式">
            <button
              type="button"
              :class="{ active: activePane === 'edit' }"
              @click="activePane = 'edit'"
            >编辑</button>
            <button
              type="button"
              :class="{ active: activePane === 'preview' }"
              @click="activePane = 'preview'"
            >预览</button>
          </div>
        </div>

        <div class="markdown-workspace">
          <textarea
            v-show="activePane === 'edit'"
            v-model="form.content"
            placeholder="# 标题&#10;&#10;支持 **加粗**、列表、引用、代码块和链接。"
            rows="22"
            maxlength="50000"
          ></textarea>
          <div
            v-show="activePane === 'preview'"
            class="markdown-preview markdown-body"
            v-html="renderedPreview"
          ></div>
        </div>
        <span class="char-count">{{ form.content.length }}/50000</span>
      </div>

      <div class="form-actions">
        <button type="button" class="btn-cancel" @click="router.back()">取消</button>
        <button type="submit" :disabled="loading" class="btn-primary">
          {{ loading ? '保存中...' : (isEdit ? '更新文章' : '发布文章') }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.editor-page {
  max-width: 880px;
  margin: 0 auto;
  padding: 1.5rem;
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  background: var(--c-bg-card);
  box-shadow: var(--shadow);
}

.editor-page h2 {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.3rem;
  font-size: 0.9rem;
  color: var(--c-text-secondary);
}

.required { color: var(--c-danger); }

.field-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.3rem;
}

.field-header label {
  margin-bottom: 0;
}

.editor-tabs {
  display: flex;
  border: 1px solid var(--c-border);
  border-radius: 6px;
  overflow: hidden;
  background: var(--c-bg-soft);
}

.editor-tabs button {
  padding: 0.35rem 0.8rem;
  border: 0;
  background: transparent;
  color: var(--c-text-secondary);
  cursor: pointer;
  font-size: 0.85rem;
}

.editor-tabs button.active {
  background: var(--c-primary);
  color: #fff;
}

.form-group input, .form-group select, .form-group textarea {
  width: 100%;
  padding: 0.7rem 0.85rem;
  border: 1px solid var(--c-border);
  border-radius: 6px;
  font-size: 0.95rem;
  box-sizing: border-box;
  font-family: inherit;
}

.form-group input:focus, .form-group select:focus, .form-group textarea:focus {
  outline: none;
  border-color: var(--c-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.form-group textarea {
  resize: vertical;
  line-height: 1.6;
}

.markdown-workspace {
  min-height: 440px;
}

.markdown-workspace textarea,
.markdown-preview {
  min-height: 440px;
}

.markdown-workspace textarea {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace;
}

.markdown-preview {
  width: 100%;
  padding: 0.9rem 1rem;
  border: 1px solid var(--c-border);
  border-radius: 6px;
  background: var(--c-bg-soft);
  box-sizing: border-box;
  overflow: auto;
}

.markdown-body {
  color: var(--c-text);
  line-height: 1.75;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4) {
  margin: 1.1rem 0 0.6rem;
  line-height: 1.3;
}

.markdown-body :deep(p),
.markdown-body :deep(ul),
.markdown-body :deep(ol),
.markdown-body :deep(blockquote),
.markdown-body :deep(pre),
.markdown-body :deep(table) {
  margin: 0.8rem 0;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 1.5rem;
}

.markdown-body :deep(blockquote) {
  padding: 0.2rem 1rem;
  border-left: 3px solid var(--c-primary);
  color: var(--c-text-secondary);
  background: var(--c-primary-soft);
  border-radius: 0 6px 6px 0;
}

.markdown-body :deep(code) {
  padding: 0.12rem 0.35rem;
  border: 1px solid var(--c-border);
  border-radius: 4px;
  background: var(--c-bg-card);
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
  border: 0;
  background: transparent;
  color: inherit;
}

.markdown-body :deep(img) {
  max-width: 100%;
  border-radius: var(--radius);
}

.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  display: block;
  overflow-x: auto;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid var(--c-border);
  padding: 0.5rem 0.65rem;
}

.char-count {
  display: block;
  text-align: right;
  font-size: 0.8rem;
  color: var(--c-text-muted);
  margin-top: 0.25rem;
}

.error-msg {
  background: var(--c-danger-soft);
  color: var(--c-danger);
  padding: 0.65rem 0.8rem;
  border: 1px solid rgba(220, 38, 38, 0.16);
  border-radius: 6px;
  margin-bottom: 1rem;
  font-size: 0.86rem;
  line-height: 1.5;
  overflow-wrap: anywhere;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.btn-primary {
  padding: 0.6rem 2rem;
  background: var(--c-primary);
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
}

.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-primary:hover:not(:disabled) { background: var(--c-primary-hover); }

.btn-cancel {
  padding: 0.6rem 1.5rem;
  background: var(--c-bg-card);
  border: 1px solid var(--c-border);
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
}

@media (min-width: 920px) {
  .editor-tabs {
    display: none;
  }

  .markdown-workspace {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: 1rem;
  }

  .markdown-workspace textarea,
  .markdown-preview {
    display: block !important;
  }
}

@media (max-width: 640px) {
  .editor-page {
    padding: 1rem;
  }

  .field-header {
    align-items: stretch;
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
