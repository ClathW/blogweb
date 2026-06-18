<template>
  <div class="admin-dashboard">
    <h2>后台管理</h2>
    <div class="dashboard-grid">
      <router-link to="/admin/users" class="dashboard-card">
        <h3>用户管理</h3>
        <p>查看和管理注册用户，变更用户状态</p>
      </router-link>
      <router-link to="/admin/articles" class="dashboard-card">
        <h3>文章管理</h3>
        <p>查看全站文章，处理违规内容</p>
      </router-link>
      <router-link to="/admin/comments" class="dashboard-card">
        <h3>评论管理</h3>
        <p>查看全站评论，删除违规评论</p>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard {
  max-width: 800px;
  margin: 0 auto;
}

.admin-dashboard h2 {
  margin-bottom: 1.5rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.dashboard-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1.5rem;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.dashboard-card:hover {
  border-color: #2563eb;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.1);
}

.dashboard-card h3 {
  margin-bottom: 0.5rem;
  color: #2563eb;
}

.dashboard-card p {
  color: #6b7280;
  font-size: 0.9rem;
}
</style>
