<template>
  <div class="container py-5">
    <h2 class="mb-4 text-center">Edit Menu Availability</h2>

    <div v-if="menuItems.length" class="row g-3">
      <div v-for="item in menuItems" :key="item.id" class="col-md-6 col-lg-4">
        <div class="card shadow-sm p-3 d-flex flex-column">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="fw-semibold">{{ item.name }} - ₹{{ item.price }}</span>
            <div class="form-check form-switch">
              <input 
                class="form-check-input" 
                type="checkbox" 
                v-model="item.is_available" 
                @change="updateAvailability(item)"
              />
              <label class="form-check-label">{{ item.is_available ? 'Available' : 'Unavailable' }}</label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-5">
      <i class="bi bi-inbox display-1 text-muted mb-3"></i>
      <h4 class="text-muted">No Menu Items</h4>
      <p class="text-muted">Please add items first.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'

const menuItems = ref([])

const fetchMenu = async () => {
  try {
    const response = await api.get('menu/staff/items/')
    menuItems.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []
    
    console.log('Fetched menu items:', menuItems.value) 
  } catch (err) {
    console.error('Error fetching menu:', err)
  }
}

const updateAvailability = async (item) => {
  try {
    await api.patch(`menu/staff/items/${item.id}/`, { is_available: item.is_available })
    console.log(`Updated availability for ${item.name}:`, item.is_available)
  } catch (err) {
    console.error('Error updating availability:', err)
  }
}

onMounted(fetchMenu)
</script>

<style scoped>
.card {
  border-radius: 12px;
}
</style>
