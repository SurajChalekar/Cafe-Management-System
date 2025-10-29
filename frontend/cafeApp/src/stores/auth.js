// stores/auth.js
import { defineStore } from 'pinia'
import api from '@/api/axios' // your axios instance

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,               // logged-in user object
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    isAuthenticated: false,   // true if user is logged in
    role: localStorage.getItem('role') || null,
  }),

  getters: {
    /**
     * Check if user is staff
     */
    isStaff: (state) => state.role === 'staff',

    /**
     * Check if user is a customer
     */
    isCustomer: (state) => state.role === 'customer',
  },

  actions: {
    /**
     * Login user and store tokens
     * @param {Object} credentials - { username, password }
     */
    async login(credentials) {
      try {
        const response = await api.post('/auth/login/', credentials)
        const { access, refresh, user } = response.data

        this.accessToken = access
        this.refreshToken = refresh
        this.user = user
        this.role = user.role
        this.isAuthenticated = true

        // Save tokens to localStorage
        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        localStorage.setItem('role', user.role)
        localStorage.setItem('username', user.username)

        return true
      } catch (error) {
        console.error('Login failed:', error.response?.data || error)
        throw error
      }
    },

    /**
     * Logout user (backend + local cleanup)
     */
    async logout() {
      try {
        if (this.refreshToken) {
          await api.post('/auth/logout/', { refresh: this.refreshToken })
        }
      } catch (error) {
        console.warn('Logout API failed, continuing cleanup')
      } finally {
        this.clearAuth()
      }
    },

    /**
     * Clear all auth-related state and localStorage
     */
    clearAuth() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      this.role = null
      this.isAuthenticated = false

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('role')
      localStorage.removeItem('username')

      window.location.href = '/login'
    },

    /**
     * Sync state with localStorage (e.g., on page reload)
     */
    loadFromStorage() {
      const access = localStorage.getItem('access_token')
      const refresh = localStorage.getItem('refresh_token')
      const role = localStorage.getItem('role')
      const username = localStorage.getItem('username')

      if (access && refresh && role && username) {
        this.accessToken = access
        this.refreshToken = refresh
        this.role = role
        this.isAuthenticated = true
        this.user = { username, role }
      } else {
        this.clearAuth()
      }
    },
  },
})
