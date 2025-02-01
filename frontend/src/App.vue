<script setup lang="ts">
import { computed } from 'vue';
import { useAuthStore } from './stores/auth'
import { RouterLink, RouterView, useRouter, useRoute } from 'vue-router'
import DefaultLayout from '@/views/layouts/DefaultLayout.vue'
import AnotherLayout from '@/views/layouts/AnotherLayout.vue'
import HelloWorld from '@/components/HelloWorld.vue'
import TopView from '@/components/TopView.vue'

const authStore = useAuthStore()
const router = useRouter()


const route = useRoute();
const layout = computed(() => {
  if (route.path.startsWith('/about')) {
    return AnotherLayout;
  }
  return DefaultLayout;
});

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
    <!-- <TopView /> -->
    <component :is="layout">
      <router-view></router-view>
    </component>
  <!-- <RouterView /> -->
</template>