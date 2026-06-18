import api from './index'

// User management
export function getAdminUsers(params = {}) {
  return api.get('/admin/users/', { params })
}

export function updateUserStatus(id, status) {
  return api.put(`/admin/users/${id}/status/`, { status })
}

// Article management
export function getAdminArticles(params = {}) {
  return api.get('/admin/articles/', { params })
}

export function adminDeleteArticle(id) {
  return api.delete(`/admin/articles/${id}/`)
}

// Category management
export function getAdminCategories() {
  return api.get('/admin/categories/')
}

export function createAdminCategory(data) {
  return api.post('/admin/categories/', data)
}

export function updateAdminCategory(id, data) {
  return api.put(`/admin/categories/${id}/`, data)
}

export function deleteAdminCategory(id) {
  return api.delete(`/admin/categories/${id}/`)
}

// Comment management
export function getAdminComments(params = {}) {
  return api.get('/admin/comments/', { params })
}

export function adminDeleteComment(id) {
  return api.delete(`/admin/comments/${id}/`)
}
