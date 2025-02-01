<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <header class="gnb-header">
    <div class="gnb-container">
      <RouterLink to="/" class="logo">로고</RouterLink>
      <nav class="nav-links">
        <RouterLink to="/">홈</RouterLink>
        <RouterLink to="/about">소개</RouterLink>
        <button v-if="authStore.isAuthenticated" @click="handleLogout">로그아웃</button>
        <RouterLink v-else to="/login">로그인</RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.gnb-header {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem;
}

.gnb-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: #333;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-links a {
  text-decoration: none;
  color: #333;
}

.nav-links button {
  padding: 0.5rem 1rem;
  background-color: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.nav-links a:hover,
.nav-links button:hover {
  color: #666;
}
</style> 