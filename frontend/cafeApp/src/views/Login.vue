<template>
  <div class="login-container">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-5 col-lg-4">
          <div class="card login-card shadow-lg">
            <div class="card-body p-5">
              <div class="text-center mb-4">
                <img src="@/assets/logo/images.jpeg" alt="Cafe Logo" width="80" height="80" class="d-inline-block align-text-top me-2">
                <h2 class="mt-3 fw-bold">Cafe Login</h2>
                <p class="text-muted">Welcome back!</p>
              </div>

              <form @submit.prevent="handleLogin">
                <div class="mb-3">
                  <label for="username" class="form-label">Username</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="bi bi-person"></i>
                    </span>
                    <input type="text" class="form-control" id="username" v-model="credentials.username"
                      placeholder="Enter username" required />
                  </div>
                </div>

                <div class="mb-4">
                  <label for="password" class="form-label">Password</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="bi bi-lock"></i>
                    </span>
                    <input type="password" class="form-control" id="password" v-model="credentials.password"
                      placeholder="Enter password" required />
                  </div>
                </div>

                <div v-if="error" class="alert alert-danger" role="alert">
                  <i class="bi bi-exclamation-triangle me-2"></i>
                  {{ error }}
                </div>

                <button type="submit" class="btn btn-primary w-100 py-2 fw-bold">
                  <i class="bi bi-box-arrow-in-right me-2"></i>
                  Login
                </button>
              </form>

              <!-- Register Link -->
              <div class="mt-3 text-center">
                <small class="text-muted">
                  Don't have an account?
                  <router-link to="/register">Register here</router-link>
                </small>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/store/auth'
import api from '@/api/axios'

const authStore = useAuthStore()

const credentials = ref({
  username: '',
  password: ''
})

const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  loading.value = true

  try {
    const res = await api.post('auth/login/', {
      username: credentials.value.username,
      password: credentials.value.password
    })

    console.log('Login response:', res.data)

    // Save tokens and user info
    localStorage.setItem('access_token', res.data.access)
    localStorage.setItem('refresh_token', res.data.refresh)
    localStorage.setItem('username', res.data.username)
    localStorage.setItem('role', res.data.role)

    // Update Pinia store
    authStore.checkAuth()

    // Redirect based on role (immediately) 
    if (res.data.role === 'staff') {
      window.location.href = '/orders'  // full page reload
    } else if (res.data.role === 'customer') {
      window.location.href = '/menu'
    } else {
      window.location.href = '/'
    }

  } catch (err) {
    console.error('Login failed:', err)
    error.value = err.response?.data?.detail || 'Invalid username or password'
  } finally {
    loading.value = false
  }
}


</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  background-color: #16171f;
}

.login-card {
  border: none;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.input-group-text {
  background-color: #f8f9fa;
  border-right: none;
}

.form-control {
  border-left: none;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.btn-primary {
  background-color: #16171f;
  border: none;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #0d0e13;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(22, 23, 31, 0.4);
}
</style>