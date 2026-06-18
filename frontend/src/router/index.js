import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomePage.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginPage.vue'),
    meta: { guest: true },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/RegisterPage.vue'),
    meta: { guest: true },
  },
  {
    path: '/articles/:id',
    name: 'article-detail',
    component: () => import('@/views/ArticleDetail.vue'),
  },
  {
    path: '/editor',
    name: 'editor-create',
    component: () => import('@/views/ArticleEditor.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/editor/:id',
    name: 'editor-edit',
    component: () => import('@/views/ArticleEditor.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/views/ProfilePage.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/my-articles',
    name: 'my-articles',
    component: () => import('@/views/MyArticles.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/admin',
    name: 'admin-dashboard',
    component: () => import('@/views/admin/AdminDashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/users',
    name: 'admin-users',
    component: () => import('@/views/admin/AdminUsers.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/articles',
    name: 'admin-articles',
    component: () => import('@/views/admin/AdminArticles.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/comments',
    name: 'admin-comments',
    component: () => import('@/views/admin/AdminComments.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
