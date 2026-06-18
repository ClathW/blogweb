import api from './index'

export function getCategories() {
  return api.get('/categories/')
}

export function getArticles(params = {}) {
  return api.get('/articles/', { params })
}

export function getMyArticles(params = {}) {
  return api.get('/articles/my/', { params })
}

export function getArticle(id) {
  return api.get(`/articles/${id}/`)
}

export function createArticle(data) {
  return api.post('/articles/create/', data)
}

export function updateArticle(id, data) {
  return api.put(`/articles/${id}/edit/`, data)
}

export function deleteArticle(id) {
  return api.delete(`/articles/${id}/edit/`)
}
