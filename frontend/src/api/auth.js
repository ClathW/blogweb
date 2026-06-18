import api from './index'

export function getCSRFToken() {
  return api.get('/auth/csrf/')
}

export function register(data) {
  return api.post('/auth/register/', data)
}

export function login(data) {
  return api.post('/auth/login/', data)
}

export function logout() {
  return api.post('/auth/logout/')
}

export function checkAuth() {
  return api.get('/auth/check/')
}

export function getProfile() {
  return api.get('/user/profile/')
}

export function updateProfile(data) {
  return api.put('/user/profile/', data)
}

export function changePassword(data) {
  return api.put('/user/password/', data)
}
