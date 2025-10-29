<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top shadow">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">
        <i class="bi bi-cup-hot-fill me-2"></i>
        MyCafe
      </a>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">

          <!-- Consumer Navigation -->
          <template v-if="authStore.isConsumer">
            <li class="nav-item">
              <router-link class="nav-link" to="/menu" active-class="active">
                <i class="bi bi-card-list me-1"></i>
                Menu
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/place-order" active-class="active">
                <i class="bi bi-cart-plus me-1"></i>
                Place Order
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/my-orders" active-class="active">
                <i class="bi bi-bag-check me-1"></i>
                My Orders
              </router-link>
            </li>
          </template>

          <!-- Staff Navigation -->
          <template v-if="authStore.isStaff">
            <li class="nav-item">
              <router-link class="nav-link" to="/orders" active-class="active">
                <i class="bi bi-list-check me-1"></i>
                Orders
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/edit-menu" active-class="active">
                <i class="bi bi-pencil-square me-1"></i>
                Edit Menu
              </router-link>
            </li>
          </template>
          <!-- User Info and Logout -->
          <li class="nav-item dropdown" v-if="authStore.isAuthenticated">
            <a class="nav-link dropdown-toggle d-flex align-items-center" href="#" id="userDropdown" role="button"
              data-bs-toggle="dropdown" aria-expanded="false">
              <i class="bi bi-person-circle me-2 fs-5"></i>
              <span>{{ authStore.username || 'User' }}</span>
            </a>

            <ul class="dropdown-menu dropdown-menu-end shadow" aria-labelledby="userDropdown">
              <li class="px-3 py-2">
                <div class="fw-semibold">{{ authStore.username || 'User' }}</div>
              </li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li>
                <button class="dropdown-item text-danger d-flex align-items-center" @click.prevent="logoutUser">
                  <i class="bi bi-box-arrow-right me-2"></i>
                  Logout
                </button>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

const authStore = useAuthStore()
const router = useRouter()

const logoutUser = async () => {
  const refreshToken = localStorage.getItem('refresh_token')
  if (!refreshToken) {
    console.warn('⚠️ No refresh token found, logging out locally.')
    authStore.logoutCleanup()
    router.replace('/login')
    return
  }

  try {
    await api.post('auth/logout/', { refresh: refreshToken })
    console.log('✅ Logout successful')
  } catch (err) {
    console.error('❌ Logout failed:', err.response?.data || err)
  } finally {
    authStore.logoutCleanup()
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    router.replace('/login')
  }
}
</script>

<style scoped>
.navbar {
  background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%) !important;
  padding: 1rem 2rem;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-weight: 600;
  font-size: 1.5rem;
  color: #fff;
  letter-spacing: 0.5px;
}

.navbar-brand i {
  color: #667eea;
}

.nav-link {
  transition: all 0.3s ease;
  margin: 0 8px;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
}

.nav-link:hover {
  transform: translateY(-2px);
  background: rgba(102, 126, 234, 0.1);
  color: #667eea !important;
}

.nav-link.active {
  color: #667eea !important;
  font-weight: 600;
  background: rgba(102, 126, 234, 0.15);
}

.dropdown-menu {
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 0.5rem;
}

.dropdown-item {
  border-radius: 6px;
  padding: 0.5rem 1rem;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background-color: rgba(102, 126, 234, 0.1);
  color: #667eea;
}

.dropdown-item i {
  color: #667eea;
}
</style>
