<template>
  <div class="min-vh-100" style="background: #16171f;">
    <div class="container py-5">
      <!-- Header Section -->
      <div class="text-center mb-5">
        <div class="mb-3">
          <i class="bi bi-menu-button-wide display-4 text-white"></i>
        </div>
        <h1 class="display-5 fw-bold text-white mb-2">Menu Availability</h1>
        <p class="text-white-50 fs-5">Manage your menu items in real-time</p>
      </div>

      <!-- Menu Items Grid -->
      <div v-if="menuItems.length" class="row g-4">
        <div 
          v-for="(item, index) in menuItems" 
          :key="item.id" 
          class="col-md-6 col-lg-4"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div 
            class="card menu-card h-100 border-0 shadow-lg"
            :class="{ 'unavailable': !item.is_available }"
          >
            <div class="card-body p-4">
              <!-- Item Header -->
              <div class="d-flex justify-content-between align-items-start mb-3">
                <div class="flex-grow-1">
                  <h5 class="card-title mb-1 fw-bold">{{ item.name }}</h5>
                  <div class="d-flex align-items-center gap-2">
                    <span class="badge price-badge">₹{{ item.price }}</span>
                  </div>
                </div>
                <div class="status-icon" :class="{ 'active': item.is_available }">
                  <i :class="item.is_available ? 'bi bi-check-circle-fill' : 'bi bi-x-circle-fill'"></i>
                </div>
              </div>

              <!-- Toggle Switch -->
              <div class="availability-toggle mt-4">
                <div class="form-check form-switch d-flex align-items-center justify-content-between p-3 rounded-3" style="background: #f8f9fa;">
                  <label class="form-check-label fw-semibold" style="cursor: pointer;">
                    <i :class="item.is_available ? 'bi bi-lightning-charge-fill text-success' : 'bi bi-moon-fill text-muted'" class="me-2"></i>
                    {{ item.is_available ? 'Available Now' : 'Currently Off' }}
                  </label>
                  <input 
                    class="form-check-input custom-switch m-0" 
                    type="checkbox" 
                    v-model="item.is_available" 
                    @change="updateAvailability(item)"
                    style="cursor: pointer; width: 3rem; height: 1.5rem;"
                  />
                </div>
              </div>
            </div>

            <!-- Animated background -->
            <div class="card-glow"></div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state text-center py-5">
        <div class="empty-icon-wrapper mb-4">
          <i class="bi bi-inbox display-1"></i>
        </div>
        <h3 class="fw-bold mb-2">No Menu Items Yet</h3>
        <p class="text-white-50 mb-4">Start by adding some delicious items to your menu</p>
        <button class="btn btn-light btn-lg px-4 shadow-sm">
          <i class="bi bi-plus-circle me-2"></i>Add First Item
        </button>
      </div>
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
    // Revert on error
    item.is_available = !item.is_available
  }
}

onMounted(fetchMenu)
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css');

/* Card Animations */
.col-md-6, .col-lg-4 {
  animation: fadeInUp 0.6s ease-out backwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Menu Card Styling */
.menu-card {
  background: white;
  border-radius: 20px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.menu-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15) !important;
}

.menu-card.unavailable {
  opacity: 0.7;
}

.menu-card.unavailable:hover {
  opacity: 0.85;
}

/* Animated Glow Effect */
.card-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.menu-card:hover .card-glow {
  opacity: 1;
}

/* Price Badge */
.price-badge {
  background: linear-gradient(135deg, #191f39 0%, #4b4352 100%);
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
}

/* Status Icon */
.status-icon {
  font-size: 1.8rem;
  transition: all 0.3s ease;
  color: #e0e0e0;
}

.status-icon.active {
  color: #10b981;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

/* Custom Switch */
.custom-switch:checked {
  background-color: #10b981;
  border-color: #10b981;
}

.custom-switch:focus {
  box-shadow: 0 0 0 0.25rem rgba(16, 185, 129, 0.25);
}

/* Empty State */
.empty-state {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 4rem 2rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.empty-icon-wrapper {
  width: 120px;
  height: 120px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.empty-state h3 {
  color: white;
}

/* Responsive */
@media (max-width: 768px) {
  .display-5 {
    font-size: 2rem;
  }
  
  .menu-card {
    margin-bottom: 1rem;
  }
}

/* Loading State Animation */
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}
</style>