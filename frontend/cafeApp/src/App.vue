<template>
  <div id="app">
    <!-- Navbar visible only if user is authenticated -->
    <Navbar />

    <!-- Main content -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- Optional global loader -->
    <div v-if="loading" class="global-loader">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from './store/auth'
import Navbar from './components/Navbar.vue'

const authStore = useAuthStore()
const loading = ref(true)

// Check authentication on mount
onMounted(async () => {
  await authStore.checkAuth()
  loading.value = false
})

</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f5f5f5;
  min-height: 100vh;
}

#app {
  min-height: 100vh;
}

/* Space for fixed navbar */
.main-content {
  padding-top: 106px;
  min-height: 100vh;
}

/* Optional global loader styling */
.global-loader {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
</style>
