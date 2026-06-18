import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'

// Mock the API modules
vi.mock('@/api/auth', () => ({
  getCSRFToken: vi.fn(),
  login: vi.fn(),
  register: vi.fn(),
  logout: vi.fn(),
  checkAuth: vi.fn(),
  getProfile: vi.fn(),
  updateProfile: vi.fn(),
  changePassword: vi.fn(),
}))

import * as authApi from '@/api/auth'

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    authApi.getCSRFToken.mockResolvedValue({ data: { message: 'CSRF cookie set' } })
  })

  describe('checkAuth', () => {
    it('sets user when authenticated', async () => {
      const mockUser = { id: 1, username: 'test', email: 'test@example.com', role: 'user', status: 'active' }
      authApi.checkAuth.mockResolvedValue({ data: { user: mockUser } })

      const store = useAuthStore()
      const result = await store.checkAuth()

      expect(result).toBe(true)
      expect(authApi.getCSRFToken).toHaveBeenCalled()
      expect(store.user).toEqual(mockUser)
      expect(store.isLoggedIn).toBe(true)
    })

    it('sets user to null when not authenticated', async () => {
      authApi.checkAuth.mockRejectedValue(new Error('Unauthorized'))

      const store = useAuthStore()
      const result = await store.checkAuth()

      expect(result).toBe(false)
      expect(store.user).toBeNull()
      expect(store.isLoggedIn).toBe(false)
    })
  })

  describe('clearAuth', () => {
    it('clears user and can reset initialization state', async () => {
      authApi.checkAuth.mockResolvedValue({ data: { user: { id: 1, username: 'test' } } })

      const store = useAuthStore()
      await store.checkAuth()
      expect(store.initialized).toBe(true)

      store.clearAuth({ resetInitialized: true })

      expect(store.user).toBeNull()
      expect(store.initialized).toBe(false)
    })
  })

  describe('loginUser', () => {
    it('sets user on successful login', async () => {
      const mockUser = { id: 1, username: 'test', role: 'user' }
      authApi.login.mockResolvedValue({ data: { user: mockUser, message: '登录成功' } })

      const store = useAuthStore()
      const result = await store.loginUser({ username: 'test', password: 'test123456' })

      expect(result.user).toEqual(mockUser)
      expect(store.user).toEqual(mockUser)
    })

    it('throws error on failed login', async () => {
      authApi.login.mockRejectedValue({ response: { data: { message: '用户名或密码错误' } } })

      const store = useAuthStore()
      await expect(store.loginUser({ username: 'test', password: 'wrong' }))
        .rejects.toBeTruthy()
    })
  })

  describe('registerUser', () => {
    it('calls register API', async () => {
      authApi.register.mockResolvedValue({ data: { message: '注册成功' } })

      const store = useAuthStore()
      const result = await store.registerUser({
        username: 'newuser',
        password: 'test123456',
        confirm_password: 'test123456',
        email: 'new@test.com',
      })

      expect(result.message).toBe('注册成功')
      expect(authApi.register).toHaveBeenCalledWith({
        username: 'newuser',
        password: 'test123456',
        confirm_password: 'test123456',
        email: 'new@test.com',
      })
    })
  })

  describe('logoutUser', () => {
    it('clears user state after logout', async () => {
      authApi.checkAuth.mockResolvedValue({ data: { user: { id: 1, username: 'test' } } })
      authApi.logout.mockResolvedValue({ data: { message: '已登出' } })

      const store = useAuthStore()
      await store.checkAuth()
      expect(store.isLoggedIn).toBe(true)

      await store.logoutUser()
      expect(store.user).toBeNull()
      expect(store.isLoggedIn).toBe(false)
    })
  })

  describe('isAdmin', () => {
    it('returns true for admin role', async () => {
      authApi.checkAuth.mockResolvedValue({
        data: { user: { id: 1, username: 'admin', email: '', role: 'admin', status: 'active' } }
      })

      const store = useAuthStore()
      await store.checkAuth()

      expect(store.isAdmin).toBe(true)
    })

    it('returns false for user role', async () => {
      authApi.checkAuth.mockResolvedValue({
        data: { user: { id: 2, username: 'user', email: '', role: 'user', status: 'active' } }
      })

      const store = useAuthStore()
      await store.checkAuth()

      expect(store.isAdmin).toBe(false)
    })
  })
})
