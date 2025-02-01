import { defineStore } from 'pinia'
import api from '../utils/api'
import { API_ROUTES } from '../constants/api'

interface User {
  id: number
  email: string
  username: string
}

interface AuthState {
  user: User | null
  token: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: localStorage.getItem('token')
  }),

  actions: {
    async login(email: string, password: string) {
      try {
        const formData = new FormData()
        formData.append('username', email)
        formData.append('password', password)
        
        const response = await api.post(API_ROUTES.AUTH.LOGIN, formData)
        this.token = response.data.access_token
        localStorage.setItem('token', this.token)
        return true
      } catch (error) {
        console.error('Login failed:', error)
        return false
      }
    },

    async register(email: string, username: string, password: string) {
      try {
        const response = await api.post(API_ROUTES.AUTH.REGISTER, {
          email,
          username,
          password
        })
        return response.data
      } catch (error) {
        console.error('Registration failed:', error)
        return null
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
    }
  }
}) 