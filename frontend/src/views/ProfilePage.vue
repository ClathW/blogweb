<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

// Profile edit
const profileForm = reactive({
  bio: auth.user?.bio || '',
  avatar: auth.user?.avatar || '',
})
const profileMsg = ref('')

async function handleUpdateProfile() {
  try {
    const result = await auth.updateProfile(profileForm)
    profileMsg.value = result.message || '更新成功'
    // Re-check auth to refresh user state
    await auth.checkAuth()
  } catch (err) {
    profileMsg.value = err.response?.data?.message || '更新失败'
  }
}

// Password change
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: '',
})
const passwordMsg = ref('')

async function handleChangePassword() {
  passwordMsg.value = ''
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    passwordMsg.value = '两次密码输入不一致'
    return
  }
  try {
    const result = await auth.changePassword(passwordForm)
    passwordMsg.value = result.message || '修改成功'
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  } catch (err) {
    passwordMsg.value = err.response?.data?.message || '密码修改失败'
  }
}
</script>

<template>
  <div class="profile-page">
    <h2>个人中心</h2>

    <div class="profile-info card">
      <h3>基本信息</h3>
      <p><strong>用户名：</strong>{{ auth.user?.username }}</p>
      <p><strong>邮箱：</strong>{{ auth.user?.email }}</p>
      <p><strong>角色：</strong>{{ auth.user?.role === 'admin' ? '管理员' : '普通用户' }}</p>
      <p><strong>注册时间：</strong>{{ new Date(auth.user?.date_joined).toLocaleDateString() }}</p>
    </div>

    <div class="card">
      <h3>修改资料</h3>
      <div v-if="profileMsg" class="msg">{{ profileMsg }}</div>
      <div class="form-group">
        <label>个人简介</label>
        <textarea v-model="profileForm.bio" rows="3" maxlength="200" placeholder="介绍一下自己（200字以内）"></textarea>
      </div>
      <div class="form-group">
        <label>头像URL</label>
        <input v-model="profileForm.avatar" type="url" placeholder="头像图片地址" />
      </div>
      <button class="btn-primary" @click="handleUpdateProfile">保存修改</button>
    </div>

    <div class="card">
      <h3>修改密码</h3>
      <div v-if="passwordMsg" class="msg">{{ passwordMsg }}</div>
      <div class="form-group">
        <label>原密码</label>
        <input v-model="passwordForm.old_password" type="password" />
      </div>
      <div class="form-group">
        <label>新密码</label>
        <input v-model="passwordForm.new_password" type="password" placeholder="6-20位新密码" />
      </div>
      <div class="form-group">
        <label>确认新密码</label>
        <input v-model="passwordForm.confirm_password" type="password" />
      </div>
      <button class="btn-primary" @click="handleChangePassword">修改密码</button>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  max-width: 720px;
  margin: 0 auto;
}

.profile-page h2 {
  margin-bottom: 1.5rem;
}

.card {
  background: var(--c-bg-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: var(--shadow);
}

.card h3 {
  margin-bottom: 1rem;
}

.profile-info p {
  margin: 0.5rem 0;
  color: var(--c-text-secondary);
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

.form-group input, .form-group textarea {
  width: 100%;
  padding: 0.7rem 0.85rem;
  border: 1px solid var(--c-border);
  border-radius: 6px;
  font-size: 0.95rem;
  box-sizing: border-box;
}

.form-group input:focus, .form-group textarea:focus {
  outline: none;
  border-color: var(--c-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.msg {
  padding: 0.5rem 0.8rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  background: var(--c-success-soft);
  color: var(--c-success);
}

.btn-primary {
  padding: 0.6rem 1.5rem;
  background: var(--c-primary);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  cursor: pointer;
}

.btn-primary:hover { background: var(--c-primary-hover); }
</style>
