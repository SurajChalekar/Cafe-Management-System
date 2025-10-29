// stores/cart.js
import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [], // { id, name, price, quantity }
  }),

  getters: {
    totalAmount: (state) =>
      state.items.reduce((sum, item) => sum + item.price * item.quantity, 0),

    itemCount: (state) =>
      state.items.reduce((count, item) => count + item.quantity, 0),
  },

  actions: {
    /**
     * Add an item to the cart
     * @param {Object} item - { id, name, price }
     */
    addToCart(item) {
      const existing = this.items.find(i => i.id === item.id)
      if (existing) {
        existing.quantity++
      } else {
        this.items.push({ ...item, quantity: 1 })
      }
    },

    /**
     * Remove an item completely from the cart
     * @param {Number} itemId
     */
    removeFromCart(itemId) {
      this.items = this.items.filter(i => i.id !== itemId)
    },

    /**
     * Increment quantity of an item
     * @param {Number} itemId
     */
    incrementItem(itemId) {
      const item = this.items.find(i => i.id === itemId)
      if (item) item.quantity++
    },

    /**
     * Decrement quantity of an item
     * Removes item if quantity reaches zero
     * @param {Number} itemId
     */
    decrementItem(itemId) {
      const item = this.items.find(i => i.id === itemId)
      if (item) {
        item.quantity--
        if (item.quantity <= 0) this.removeFromCart(itemId)
      }
    },

    /**
     * Clear the entire cart
     */
    clearCart() {
      this.items = []
    },
  },
})
