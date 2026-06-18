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

// Comment management
export function getAdminComments(params = {}) {
  return api.get('/admin/comments/', { params })
}

export function adminDeleteComment(id) {
  return api.delete(`/admin/comments/${id}/`)
}
