<template>
  <div class="admin-dashboard">
    <h2>后台管理</h2>
    <div class="dashboard-grid">
      <router-link to="/manage/users" class="dashboard-card">
        <h3>用户管理</h3>
        <p>查看和管理注册用户，变更用户状态</p>
      </router-link>
      <router-link to="/manage/articles" class="dashboard-card">
        <h3>文章管理</h3>
        <p>查看全站文章，处理违规内容</p>
      </router-link>
      <router-link to="/manage/comments" class="dashboard-card">
        <h3>评论管理</h3>
        <p>查看全站评论，删除违规评论</p>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard {
  max-width: 920px;
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
  background: var(--c-bg-card);
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  padding: 1.5rem;
  text-decoration: none;
  color: inherit;
  box-shadow: var(--shadow);
  transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
}

.dashboard-card:hover {
  border-color: rgba(37, 99, 235, 0.32);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.dashboard-card h3 {
  margin-bottom: 0.5rem;
  color: var(--c-primary);
}

.dashboard-card p {
  color: var(--c-text-secondary);
  font-size: 0.9rem;
}
</style>
