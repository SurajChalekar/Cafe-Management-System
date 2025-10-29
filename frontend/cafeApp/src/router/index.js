import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

// Views
import Login from '@/views/Login.vue'
import Menu from '@/views/Menu.vue'
import PlaceOrder from '@/views/PlaceOrder.vue'
import Orders from '@/views/Orders.vue'
import CustomerOrders from '@/views/CustomerOrders.vue'
import Register from '@/views/Register.vue'
import EditMenu from '@/views/MenuEdit.vue'

const routes = [
  { path: '/', redirect: '/login' },

  // Auth routes
  { path: '/login', name: 'Login', component: Login, meta: { requiresAuth: false } },
  { path: '/register', name: 'Register', component: Register, meta: { requiresAuth: false } },

  // Customer routes
  { path: '/menu', name: 'Menu', component: Menu, meta: { requiresAuth: true, roles: ['customer'] } },
  { path: '/place-order', name: 'PlaceOrder', component: PlaceOrder, meta: { requiresAuth: true, roles: ['customer'] } },
  { path: '/my-orders', name: 'CustomerOrders', component: CustomerOrders, meta: { requiresAuth: true, roles: ['customer'] } },

  // Staff routes
  { path: '/orders', name: 'Orders', component: Orders, meta: { requiresAuth: true, roles: ['staff'] } },
  { path: '/edit-menu', name: 'EditMenu', component: EditMenu, meta: { requiresAuth: true, roles: ['staff'] } },

  // Catch-all
  { path: '/:pathMatch(.*)*', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = !!authStore.accessToken
  const role = authStore.isStaff ? 'staff' : authStore.isConsumer ? 'customer' : null

  // Not authenticated → redirect to login
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login')
  }

  // Role-based protection
  if (to.meta.roles && !to.meta.roles.includes(role)) {
    if (role === 'staff') return next('/orders')
    if (role === 'customer') return next('/menu')
    return next('/login')
  }

  // Already logged in but visiting login page → redirect to role default
  if (to.path === '/login' && isAuthenticated) {
    if (role === 'staff') return next('/orders')
    if (role === 'customer') return next('/menu')
  }

  next()
})

export default router
