import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/About.vue'),
    },
    {
      path: '/login',
      name: 'Login',
      // component: Login
      component: () => import('../views/Login.vue'),
    },
    {
      path: '/editor',
      name: 'Editor',
      // component: Editor,
      component: () => import('../views/Editor.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/agenda',
      name: 'Agenda',
      // component: Agenda,
      component: () => import('../views/Agenda.vue'),
      meta: { requiresAuth: true }
    }
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.token) {
    next('/login')
  } else {
    next()
  }
})

export default router
