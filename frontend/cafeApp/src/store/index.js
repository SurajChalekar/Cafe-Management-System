import { createPinia } from 'pinia';
import { defineStore } from 'pinia';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token'),
    isAuthenticated: false,
  }),
  
  actions: {
    async login(credentials) {
      const response = await api.login(credentials);
      this.token = response.data.access;
      localStorage.setItem('access_token', this.token);
      this.isAuthenticated = true;
    },
    
    logout() {
      this.user = null;
      this.token = null;
      this.isAuthenticated = false;
      localStorage.removeItem('access_token');
    },
  },
});

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
  }),
  
  getters: {
    totalAmount: (state) => {
      return state.items.reduce((sum, item) => 
        sum + (item.price * item.quantity), 0
      );
    },
  },
  
  actions: {
    addItem(item) {
      const existing = this.items.find(i => i.id === item.id);
      if (existing) {
        existing.quantity++;
      } else {
        this.items.push({ ...item, quantity: 1 });
      }
    },
    
    removeItem(itemId) {
      this.items = this.items.filter(i => i.id !== itemId);
    },
    
    clearCart() {
      this.items = [];
    },
  },
});

export default createPinia();