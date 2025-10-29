<template>
  <div class="container mt-5" style="max-width: 400px;">
    <h3 class="text-center mb-4">Register</h3>
    <div class="card p-4 shadow">
      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div class="mb-3">
        <label>First Name</label>
        <input v-model="first_name" class="form-control" />
      </div>

      <div class="mb-3">
        <label>Last Name</label>
        <input v-model="last_name" class="form-control" />
      </div>

      <div class="mb-3">
        <label>Username</label>
        <input v-model="username" class="form-control" />
      </div>

      <div class="mb-3">
        <label>Email</label>
        <input v-model="email" class="form-control" />
      </div>

      <div class="mb-3">
        <label>Password</label>
        <input type="password" v-model="password" class="form-control" />
      </div>

      <div class="mb-3">
        <label>Confirm Password</label>
        <input type="password" v-model="password2" class="form-control" />
      </div>


      <button @click="register" class="btn btn-success w-100" :disabled="loading">
        {{ loading ? 'Registering...' : 'Register' }}
      </button>

      <p class="text-center mt-3">
        Already have an account? <router-link to="/login">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

const router = useRouter()

const first_name = ref('')
const last_name = ref('')
const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const role = ref('customer')
const error = ref('')
const loading = ref(false)

const register = async () => {
  error.value = ''
  loading.value = true

  try {
    const payload = {
      first_name: first_name.value,
      last_name: last_name.value,
      username: username.value,
      email: email.value,
      password: password.value,
      password2: password2.value,
      is_staff: role.value === 'staff'
    }

    console.log('Register payload:', payload)

    const res = await api.post('auth/register/', payload)
    console.log('✅ Registration successful:', res.data)

    router.push('/login')
  } catch (err) {
    console.error('❌ Registration failed:', err)
    if (err.response?.data) {
      error.value = JSON.stringify(err.response.data)
    } else {
      error.value = 'Registration failed. Please check your input.'
    }
  } finally {
    loading.value = false
  }
}
</script>
