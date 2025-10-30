<template>
  <nav class="navbar navbar-expand-lg fixed-top shadow" style="background-color: #f5fefd;">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">
        <img src="@/assets/logo/images.jpeg" alt="Cafe Logo" width="50" height="50" class="d-inline-block align-text-top me-2">
        CafeApp
      </a>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <!-- Centered Navigation Container -->
        <div class="nav-center-wrapper">
          <ul class="navbar-nav">
            <!-- Consumer Navigation -->
            <template v-if="authStore.isConsumer">
              <li class="nav-item">
                <router-link class="nav-link" to="/menu" active-class="active">
                  Menu
                </router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/place-order" active-class="active">
                  Place Order
                </router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/my-orders" active-class="active">
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
          </ul>
        </div>

        <!-- User Profile - Right Side -->
        <ul class="navbar-nav profile-nav">
          <li class="nav-item dropdown" v-if="authStore.isAuthenticated">
            <a class="nav-link d-flex align-items-center" href="#" id="userDropdown" role="button"
              data-bs-toggle="dropdown" aria-expanded="false">
              <i class="bi bi-person-circle fs-4"></i>
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
  padding: 1.5rem 2.5rem;
  min-height: 80px;
}

.navbar-collapse {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-center-wrapper {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.profile-nav {
  margin-left: auto;
}

.navbar-brand {
  font-weight: 600;
  font-size: 1.8rem;
  color: #000000;
  letter-spacing: 0.5px;
}

.navbar-brand i {
  color: #626262;
  font-size: 2rem;
}

.nav-link {
  transition: all 0.3s ease;
  margin: 0 12px;
  padding: 0.6rem 1.2rem;
  font-weight: 500;
  font-size: 1.1rem;
  position: relative;
  color: #000000 !important;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background-color: #000000;
  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 80%;
}

.nav-link.active {
  font-weight: 600;
}

.nav-link.active::after {
  width: 80%;
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

@media (max-width: 991px) {
  .nav-center-wrapper {
    position: static;
    transform: none;
    width: 100%;
  }
  
  .profile-nav {
    margin-left: 0;
  }
}
</style>