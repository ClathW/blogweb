import axios from 'axios'

let authRejectedHandler = null

export function setAuthRejectedHandler(handler) {
  authRejectedHandler = handler
}

const api = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Read CSRF token from cookie and attach to mutable requests
function getCSRFToken() {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]*)/)
  return match ? match[1] : ''
}

api.interceptors.request.use((config) => {
  const method = config.method?.toLowerCase()
  if (method === 'post' || method === 'put' || method === 'patch' || method === 'delete') {
    const token = getCSRFToken()
    if (token) {
      config.headers['X-CSRFToken'] = token
    }
  }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 || error.response?.status === 403) {
      authRejectedHandler?.()
    }
    return Promise.reject(error)
  }
)

export default api
