<template>
  <div class="not-found">
    <h1>404</h1>
    <p>页面不存在</p>
    <router-link to="/">返回首页</router-link>
  </div>
</template>

<style scoped>
.not-found {
  max-width: 520px;
  margin: 8vh auto 0;
  padding: 2.5rem;
  text-align: center;
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  background: var(--c-bg-card);
  box-shadow: var(--shadow);
}

.not-found h1 {
  font-size: 4rem;
  line-height: 1;
  color: var(--c-primary);
}

.not-found p {
  margin: 1rem 0 1.5rem;
  color: var(--c-text-secondary);
}

.not-found a {
  display: inline-block;
  padding: 0.55rem 1.2rem;
  border-radius: 6px;
  background: var(--c-primary);
  color: #fff;
}
</style>
