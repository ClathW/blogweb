import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authApi from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(false)
  const initialized = ref(false)

  const isLoggedIn = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function checkAuth() {
    loading.value = true
    try {
      const res = await authApi.checkAuth()
      user.value = res.data.user
      return true
    } catch {
      user.value = null
      return false
    } finally {
      loading.value = false
      initialized.value = true
    }
  }

  async function loginUser(credentials) {
    const res = await authApi.login(credentials)
    user.value = res.data.user
    return res.data
  }

  async function registerUser(data) {
    const res = await authApi.register(data)
    return res.data
  }

  async function logoutUser() {
    await authApi.logout()
    user.value = null
  }

  async function fetchProfile() {
    const res = await authApi.getProfile()
    user.value = res.data
    return res.data
  }

  async function updateProfile(data) {
    const res = await authApi.updateProfile(data)
    user.value = res.data.user
    return res.data
  }

  async function changePassword(data) {
    const res = await authApi.changePassword(data)
    return res.data
  }

  return {
    user,
    loading,
    initialized,
    isLoggedIn,
    isAdmin,
    checkAuth,
    loginUser,
    registerUser,
    logoutUser,
    fetchProfile,
    updateProfile,
    changePassword,
  }
})
