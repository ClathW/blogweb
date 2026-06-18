<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const form = reactive({
  username: '',
  password: '',
  confirm_password: '',
  email: '',
})
const errors = reactive({})
const loading = ref(false)

function validate() {
  Object.keys(errors).forEach(k => delete errors[k])

  if (!form.username || form.username.length < 3 || form.username.length > 20) {
    errors.username = '用户名长度须为3-20个字符'
  } else if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(form.username)) {
    errors.username = '用户名仅支持字母、数字和下划线，首字符须为字母或下划线'
  }

  if (!form.password || form.password.length < 6 || form.password.length > 20) {
    errors.password = '密码长度须为6-20个字符'
  }

  if (form.password !== form.confirm_password) {
    errors.confirm_password = '两次密码输入不一致'
  }

  if (!form.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = '请输入有效的邮箱地址'
  }

  return Object.keys(errors).length === 0
}

async function handleRegister() {
  if (!validate()) return
  loading.value = true
  try {
    await auth.registerUser(form)
    alert('注册成功，请登录')
    router.push('/login')
  } catch (err) {
    if (err.response?.status === 400 && err.response.data.errors) {
      Object.assign(errors, err.response.data.errors)
      // Flatten list errors
      for (const key in errors) {
        if (Array.isArray(errors[key])) {
          errors[key] = errors[key].join('\n')
        }
      }
    } else {
      alert(err.response?.data?.message || '注册失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>用户名 <span class="required">*</span></label>
          <input v-model="form.username" type="text" placeholder="3-20位字母、数字或下划线" />
          <span v-if="errors.username" class="field-error">{{ errors.username }}</span>
        </div>
        <div class="form-group">
          <label>邮箱 <span class="required">*</span></label>
          <input v-model="form.email" type="email" placeholder="请输入邮箱地址" />
          <span v-if="errors.email" class="field-error">{{ errors.email }}</span>
        </div>
        <div class="form-group">
          <label>密码 <span class="required">*</span></label>
          <input v-model="form.password" type="password" placeholder="6-20位密码" />
          <span v-if="errors.password" class="field-error">{{ errors.password }}</span>
        </div>
        <div class="form-group">
          <label>确认密码 <span class="required">*</span></label>
          <input v-model="form.confirm_password" type="password" placeholder="再次输入密码" />
          <span v-if="errors.confirm_password" class="field-error">{{ errors.confirm_password }}</span>
        </div>
        <button type="submit" :disabled="loading" class="btn-primary">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
      <p class="switch-link">
        已有账号？<router-link to="/login">立即登录</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 68vh;
}

.auth-card {
  background: var(--c-bg-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  padding: 2.25rem;
  width: 100%;
  max-width: 430px;
  box-shadow: var(--shadow-md);
}

.auth-card h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.65rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.3rem;
  font-size: 0.9rem;
  color: var(--c-text-secondary);
}

.required { color: var(--c-danger); }

.form-group input {
  width: 100%;
  padding: 0.7rem 0.85rem;
  border: 1px solid var(--c-border);
  border-radius: 6px;
  font-size: 0.95rem;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: var(--c-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.field-error {
  display: flex;
  align-items: flex-start;
  gap: 0.4rem;
  color: var(--c-danger);
  font-size: 0.84rem;
  line-height: 1.5;
  margin-top: 0.5rem;
  padding: 0.5rem 0.65rem;
  border: 1px solid rgba(220, 38, 38, 0.16);
  border-radius: 6px;
  background: rgba(254, 226, 226, 0.58);
  overflow-wrap: anywhere;
  white-space: pre-line;
}

.field-error::before {
  content: "!";
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  width: 1rem;
  height: 1rem;
  margin-top: 0.12rem;
  border-radius: 50%;
  background: var(--c-danger);
  color: #fff;
  font-size: 0.72rem;
  font-weight: 700;
  line-height: 1;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background: var(--c-primary);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 0.5rem;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary:hover:not(:disabled) {
  background: var(--c-primary-hover);
}

.switch-link {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.9rem;
  color: var(--c-text-secondary);
}

.switch-link a { color: var(--c-primary); }
</style>
