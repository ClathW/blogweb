<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import {
  createAdminCategory,
  deleteAdminCategory,
  getAdminCategories,
  updateAdminCategory,
} from '@/api/admin'

const categories = ref([])
const loading = ref(false)
const saving = ref(false)
const editingId = ref(null)
const form = reactive({
  name: '',
  description: '',
})

const isEditing = computed(() => editingId.value !== null)

function resetForm() {
  editingId.value = null
  form.name = ''
  form.description = ''
}

async function fetchCategories() {
  loading.value = true
  try {
    const res = await getAdminCategories()
    categories.value = res.data
  } finally {
    loading.value = false
  }
}

function startEdit(category) {
  editingId.value = category.id
  form.name = category.name
  form.description = category.description || ''
}

async function submitForm() {
  if (!form.name.trim()) {
    alert('分类名称不能为空')
    return
  }

  saving.value = true
  try {
    const payload = {
      name: form.name.trim(),
      description: form.description.trim(),
    }
    if (isEditing.value) {
      await updateAdminCategory(editingId.value, payload)
    } else {
      await createAdminCategory(payload)
    }
    resetForm()
    await fetchCategories()
  } catch (err) {
    const errors = err.response?.data?.errors
    const message = errors?.name?.[0] || err.response?.data?.message || '保存失败'
    alert(message)
  } finally {
    saving.value = false
  }
}

async function handleDelete(category) {
  const message = `确定删除分类「${category.name}」吗？相关文章不会被删除，但会变为未分类。`
  if (!confirm(message)) return

  try {
    await deleteAdminCategory(category.id)
    if (editingId.value === category.id) resetForm()
    await fetchCategories()
  } catch (err) {
    alert(err.response?.data?.message || '删除失败')
  }
}

onMounted(fetchCategories)
</script>

<template>
  <div class="admin-categories">
    <h2>分类管理</h2>

    <form class="category-form" @submit.prevent="submitForm">
      <input v-model="form.name" maxlength="50" placeholder="分类名称" />
      <input v-model="form.description" maxlength="200" placeholder="分类描述" />
      <button type="submit" :disabled="saving">
        {{ isEditing ? '保存' : '创建' }}
      </button>
      <button v-if="isEditing" type="button" class="btn-secondary" @click="resetForm">
        取消
      </button>
    </form>

    <div v-if="loading" class="loading">加载中...</div>

    <table v-else class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>名称</th>
          <th>描述</th>
          <th>已发布文章</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="category in categories" :key="category.id">
          <td>{{ category.id }}</td>
          <td>{{ category.name }}</td>
          <td>{{ category.description || '-' }}</td>
          <td>{{ category.article_count }}</td>
          <td class="actions">
            <button @click="startEdit(category)">编辑</button>
            <button class="btn-danger" @click="handleDelete(category)">删除</button>
          </td>
        </tr>
        <tr v-if="categories.length === 0">
          <td colspan="5" class="empty">暂无分类</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.admin-categories {
  max-width: 1080px;
  margin: 0 auto;
}

.admin-categories h2 {
  margin-bottom: 1.5rem;
}

.category-form {
  display: grid;
  grid-template-columns: minmax(160px, 220px) 1fr auto auto;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding: 0.9rem;
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  background: var(--c-bg-card);
  box-shadow: var(--shadow);
}

.category-form input {
  min-width: 0;
  padding: 0.5rem 0.8rem;
  border: 1px solid var(--c-border);
  border-radius: 6px;
  background: var(--c-control-bg);
  color: var(--c-text);
  font-size: 0.9rem;
}

.category-form button,
.actions button {
  padding: 0.5rem 0.9rem;
  border: 1px solid var(--c-border);
  border-radius: 6px;
  background: var(--c-primary);
  color: #fff;
  cursor: pointer;
  font-size: 0.85rem;
}

.category-form button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.category-form .btn-secondary,
.actions button {
  background: var(--c-control-bg);
  color: var(--c-text);
}

.loading {
  text-align: center;
  padding: 2rem;
  color: var(--c-text-muted);
}

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

.data-table th,
.data-table td {
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

.actions {
  display: flex;
  gap: 0.5rem;
}

.actions .btn-danger {
  border-color: rgba(220, 38, 38, 0.28);
  color: var(--c-danger);
}

.actions .btn-danger:hover {
  background: var(--c-danger-soft);
}

.empty {
  text-align: center;
  color: var(--c-text-muted);
}

@media (max-width: 800px) {
  .category-form {
    grid-template-columns: 1fr;
  }

  .data-table {
    display: block;
    overflow-x: auto;
  }
}
</style>
