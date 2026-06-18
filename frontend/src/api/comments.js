import api from './index'

export function getComments(articleId) {
  return api.get(`/articles/${articleId}/comments/`)
}

export function createComment(articleId, data) {
  return api.post(`/articles/${articleId}/comments/create/`, data)
}

export function deleteComment(id) {
  return api.delete(`/comments/${id}/`)
}
