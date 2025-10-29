import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    username: localStorage.getItem('username') || null,
    role: localStorage.getItem('role') || null,
    isStaff: false,
    isConsumer: false,
    isAuthenticated: false,
  }),

  actions: {
    // Called after login
    login(user, access, refresh) {
      this.user = user
      this.accessToken = access
      this.refreshToken = refresh
      this.username = user?.username
      this.role = user?.role || localStorage.getItem('role')

      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      if (this.username) localStorage.setItem('username', this.username)
      if (this.role) localStorage.setItem('role', this.role)

      this.checkAuth()
    },

    // Sync Pinia state with localStorage (on page reload)
    checkAuth() {
      const access = localStorage.getItem('access_token')
      const username = localStorage.getItem('username')
      const role = localStorage.getItem('role')

      if (access && username) {
        this.isAuthenticated = true
        this.username = username
        this.role = role
        this.isStaff = role === 'staff'
        this.isConsumer = role === 'customer'
      } else {
        this.isAuthenticated = false
        this.username = null
        this.role = null
        this.isStaff = false
        this.isConsumer = false
      }
    },

    // Clear everything locally and redirect
    logoutCleanup() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('username')
      localStorage.removeItem('role')

      this.user = null
      this.accessToken = null
      this.refreshToken = null
      this.isStaff = false
      this.isConsumer = false
      this.isAuthenticated = false

      window.location.href = '/login'
    },

    // Logout from backend (with safe fallback)
    async logout() {
      const refreshToken = localStorage.getItem('refresh_token')

      // Only call backend if refresh token exists
      if (refreshToken) {
        try {
          await api.post('/auth/logout/', { refresh: refreshToken })
        } catch (err) {
          console.warn('Logout API failed (ignored):', err.response?.data || err)
        }
      }

      // Always clear local storage and store
      this.logoutCleanup()
    },
  },
})
