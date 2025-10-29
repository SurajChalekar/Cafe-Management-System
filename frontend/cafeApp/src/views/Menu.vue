<template>
  <div class="menu-container">
    <div class="container py-4">

      <!-- Header & Search/Sort -->
      <div class="header-section mb-4">
        <div class="row align-items-center g-3" style="padding-bottom: 80px;">
          <div class="col-lg-6">
            <div class="header-content">
              <h1 class="page-title mb-2">
                <i class="bi bi-card-list me-2"></i>Our Menu
              </h1>
              <p class="page-subtitle mb-1">Discover our delicious offerings</p>
              <div class="item-count">
                <i class="bi bi-check-circle-fill me-1"></i>
                <span>{{ filteredItems.length }} item{{ filteredItems.length !== 1 ? 's' : '' }} available</span>
              </div>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="d-flex gap-2 align-items-stretch">
              <!-- Search -->
              <div class="search-wrapper flex-grow-1">
                <div class="input-group shadow-sm">
                  <span class="input-group-text border-0 bg-white">
                    <i class="bi bi-search text-muted"></i>
                  </span>
                  <input v-model="search" type="search" class="form-control border-0"
                    placeholder="Search menu items..." />
                </div>
              </div>

              <!-- Sort Dropdown -->
              <div class="dropdown">
                <button class="btn btn-white shadow-sm dropdown-toggle h-100" type="button" id="sortDropdown"
                  data-bs-toggle="dropdown" aria-expanded="false">
                  <i class="bi bi-sort-down me-1"></i>Sort
                </button>
                <ul class="dropdown-menu dropdown-menu-end shadow" aria-labelledby="sortDropdown">
                  <li>
                    <a class="dropdown-item" :class="{ active: sortBy === 'default' }" href="#"
                      @click.prevent="sortBy = 'default'">
                      <i class="bi bi-list-ul me-2"></i>Default Order
                    </a>
                  </li>
                  <li>
                    <hr class="dropdown-divider">
                  </li>
                  <li>
                    <a class="dropdown-item" :class="{ active: sortBy === 'price-asc' }" href="#"
                      @click.prevent="sortBy = 'price-asc'">
                      <i class="bi bi-arrow-up me-2"></i>Price: Low to High
                    </a>
                  </li>
                  <li>
                    <a class="dropdown-item" :class="{ active: sortBy === 'price-desc' }" href="#"
                      @click.prevent="sortBy = 'price-desc'">
                      <i class="bi bi-arrow-down me-2"></i>Price: High to Low
                    </a>
                  </li>
                  <li>
                    <a class="dropdown-item" :class="{ active: sortBy === 'name' }" href="#"
                      @click.prevent="sortBy = 'name'">
                      <i class="bi bi-sort-alpha-down me-2"></i>Name (A-Z)
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Categories -->
      <div class="categories-section mb-4">
        <div class="categories-scroll">
          <button v-for="cat in categories" :key="cat" class="category-btn"
            :class="{ active: selectedCategory === cat }" @click="selectCategory(cat)">
            <span class="category-name">{{ cat }}</span>
            <span v-if="categoryCounts[cat] !== undefined" class="category-count">
              {{ categoryCounts[cat] }}
            </span>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state text-center py-5">
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3 text-muted">Loading delicious items...</p>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="alert alert-danger shadow-sm d-flex align-items-center" role="alert">
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        <div>{{ errorMessage }}</div>
      </div>

      <!-- Menu Items Grid -->
      <div v-if="!loading && filteredItems.length" class="menu-grid">
        <div v-for="item in filteredItems" :key="item.id" class="menu-item-wrapper">
          <div class="menu-card">
            <!-- Image Section -->
            <div class="card-image-wrapper">
              <img :src="item.image || placeholderImage" class="card-image" :alt="item.name" loading="lazy" />
              <div class="price-badge">
                <span class="currency">₹</span>{{ item.price.toFixed(2) }}
              </div>
              <div class="category-badge">
                {{ item.categoryName }}
              </div>
            </div>

            <!-- Content Section -->
            <div class="card-content">
              <h5 class="item-title">{{ item.name }}</h5>
              <p class="item-description">{{ item.description || 'Delicious menu item' }}</p>

              <!-- Add to Cart Section -->
              <div class="card-actions">
                <div class="quantity-selector">
                  <button class="qty-btn" @click="decrementQty(item.id)" :disabled="qtyFor(item.id) <= 1">
                    <i class="bi bi-dash"></i>
                  </button>
                  <input class="qty-input" :value="qtyFor(item.id)" readonly />
                  <button class="qty-btn" @click="incrementQty(item.id)">
                    <i class="bi bi-plus"></i>
                  </button>
                </div>

                <button class="add-btn" @click="addToOrder(item)">
                  <i class="bi bi-cart-plus me-1"></i>
                  <span>Add to Cart</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !filteredItems.length" class="empty-state text-center py-5">
        <div class="empty-icon mb-3">
          <i class="bi bi-search"></i>
        </div>
        <h4 class="mb-2">No items found</h4>
        <p class="text-muted mb-4">Try adjusting your search or filter to find what you're looking for.</p>
        <button class="btn btn-primary" @click="search = ''; selectedCategory = 'All'">
          <i class="bi bi-arrow-counterclockwise me-1"></i>Reset Filters
        </button>
      </div>

      <!-- Toast Notification -->
      <div class="toast-container position-fixed bottom-0 end-0 p-3" style="z-index: 1080">
        <div v-if="showToast" class="toast show align-items-center border-0 shadow-lg"
          :class="toastType === 'success' ? 'toast-success' : 'toast-error'" role="alert" aria-live="assertive"
          aria-atomic="true">
          <div class="d-flex">
            <div class="toast-body">
              <i class="bi me-2"
                :class="toastType === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-circle-fill'"></i>
              {{ toastMessage }}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" @click="showToast = false"></button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

const router = useRouter()

// State
const selectedCategory = ref('All')
const search = ref('')
const sortBy = ref('default')
const loading = ref(false)
const errorMessage = ref('')
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('success')
const menuItems = ref([])
const categories = ref(['All'])
const categoryCounts = ref({})
const quantities = ref({})

const placeholderImage = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400"><rect width="100%" height="100%" fill="%23f8f9fa"/><text x="50%" y="50%" font-size="24" dominant-baseline="middle" text-anchor="middle" fill="%23adb5bd" font-family="system-ui">No Image Available</text></svg>'

// --- Fetch Menu Items ---
const fetchMenuItems = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const categoriesRes = await api.get('menu/categories/')
    const catsArray = categoriesRes.data.results || categoriesRes.data || []

    const categoryMap = {}
    catsArray.forEach(cat => {
      categoryMap[cat.id] = cat.name || cat.category_name || 'Uncategorized'
    })

    let allItems = []
    let nextUrl = 'menu/items/'
    while (nextUrl) {
      const res = await api.get(nextUrl)
      const data = res.data
      const results = data.results || data || []
      allItems = allItems.concat(results)
      nextUrl = data.next ? data.next.replace(api.defaults.baseURL, '') : null
    }

    const items = allItems.map(item => {
      const price = Number(item.price) || 0
      let categoryName = 'Uncategorized'

      try {
        const cat = item.category
        if (item.category_name) {
          categoryName = item.category_name
        } else if (cat) {
          if (typeof cat === 'object') {
            categoryName = cat.name || cat.category_name || 'Uncategorized'
          } else if (typeof cat === 'number') {
            categoryName = categoryMap[cat] || 'Uncategorized'
          }
        }
      } catch (e) {
        console.warn('Category parse error for item:', item, e)
      }

      return { ...item, price, categoryName }
    })

    menuItems.value = items

    const backendCategories = catsArray.map(c => c.name || c.category_name || 'Uncategorized')
    const usedCategories = [...new Set(items.map(i => i.categoryName))]
    const combinedCategories = ['All', ...new Set([...backendCategories, ...usedCategories])]
    categories.value = combinedCategories

    const counts = items.reduce((acc, it) => {
      acc[it.categoryName] = (acc[it.categoryName] || 0) + 1
      acc['All'] = (acc['All'] || 0) + 1
      return acc
    }, {})

    categories.value.forEach(c => counts[c] = counts[c] || 0)
    categoryCounts.value = counts

    items.forEach(i => {
      quantities.value[i.id] = quantities.value[i.id] || 1
    })

  } catch (error) {
    console.error('Failed to fetch menu items:', error)
    errorMessage.value = 'Failed to load menu. Please try again.'

    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      router.push('/login')
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (!token) return router.push('/login')
  fetchMenuItems()
})

// --- Computed Filtered Items ---
const filteredItems = computed(() => {
  let items = menuItems.value.slice()

  if (selectedCategory.value && selectedCategory.value !== 'All') {
    items = items.filter(i => i.categoryName === selectedCategory.value)
  }

  if (search.value.trim()) {
    const q = search.value.trim().toLowerCase()
    items = items.filter(i =>
      (i.name || '').toLowerCase().includes(q) ||
      (i.description || '').toLowerCase().includes(q)
    )
  }

  if (sortBy.value === 'price-asc') items.sort((a, b) => a.price - b.price)
  else if (sortBy.value === 'price-desc') items.sort((a, b) => b.price - a.price)
  else if (sortBy.value === 'name') items.sort((a, b) => (a.name || '').localeCompare(b.name || ''))

  return items
})

// --- Quantity Helpers ---
const qtyFor = id => quantities.value[id] || 1
const incrementQty = id => { quantities.value[id] = (quantities.value[id] || 1) + 1 }
const decrementQty = id => { quantities.value[id] = Math.max(1, (quantities.value[id] || 1) - 1) }

const selectCategory = cat => selectedCategory.value = cat

// --- Add to Cart ---
const addToOrder = async item => {
  try {
    const qty = quantities.value[item.id] || 1
    await api.post('orders/cart/add/', { item: item.id, quantity: qty })
    toastMessage.value = `${item.name} (×${qty}) added to cart!`
    toastType.value = 'success'
    showToast.value = true
    setTimeout(() => showToast.value = false, 3000)
  } catch (error) {
    console.error('Failed to add item to cart:', error)
    toastMessage.value = error.response?.status === 401 ? 'Please login to add items.' : 'Failed to add item to cart.'
    toastType.value = 'error'
    showToast.value = true
    setTimeout(() => showToast.value = false, 3000)
    if (error.response?.status === 401) router.push('/login')
  }
}
</script>

<style scoped>
/* ========== Layout ========== */
.menu-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
}

.menu-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 300px;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.1) 0%, transparent 100%);
  pointer-events: none;
}

/* ========== Header Section ========== */
.header-section {
  position: relative;
  z-index: 1;
}

.header-content {
  color: white;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.page-subtitle {
  font-size: 1.1rem;
  opacity: 0.95;
  margin: 0;
}

.item-count {
  display: inline-flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.2);
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.9rem;
  color: white;
  backdrop-filter: blur(10px);
}

/* ========== Search & Sort ========== */
.search-wrapper .input-group {
  border-radius: 12px;
  overflow: hidden;
  background: white;
}

.search-wrapper input {
  padding: 12px;
  font-size: 0.95rem;
}

.search-wrapper input:focus {
  box-shadow: none;
}

.dropdown {
  position: relative;
  z-index: 100;
}

.btn-white {
  background: white;
  color: #495057;
  border: none;
  padding: 12px 20px;
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-white:hover {
  background: #f8f9fa;
  transform: translateY(-1px);
}

.dropdown-menu {
  border: none;
  border-radius: 12px;
  padding: 8px;
  margin-top: 8px;
  z-index: 1000;
}

.dropdown-item {
  border-radius: 8px;
  padding: 10px 14px;
  transition: all 0.2s;
}

.dropdown-item:hover {
  background: #f8f9fa;
}

.dropdown-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

/* ========== Categories ========== */
.categories-section {
  position: relative;
  z-index: 1;
}

.categories-scroll {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding: 4px 0;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: thin;
}

.categories-scroll::-webkit-scrollbar {
  height: 6px;
}

.categories-scroll::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}

.categories-scroll::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 10px;
}

.category-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border-radius: 25px;
  font-weight: 500;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  backdrop-filter: blur(10px);
}

.category-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

.category-btn.active {
  background: white;
  color: #667eea;
  border-color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.category-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 8px;
  background: rgba(255, 255, 255, 0.25);
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.category-btn.active .category-count {
  background: #667eea;
  color: white;
}

/* ========== Menu Grid ========== */
.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  position: relative;
  z-index: 1;
}

.menu-item-wrapper {
  animation: fadeInUp 0.5s ease forwards;
  opacity: 0;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }

  from {
    opacity: 0;
    transform: translateY(20px);
  }
}

.menu-item-wrapper:nth-child(1) {
  animation-delay: 0.05s;
}

.menu-item-wrapper:nth-child(2) {
  animation-delay: 0.1s;
}

.menu-item-wrapper:nth-child(3) {
  animation-delay: 0.15s;
}

.menu-item-wrapper:nth-child(4) {
  animation-delay: 0.2s;
}

.menu-item-wrapper:nth-child(n+5) {
  animation-delay: 0.25s;
}

/* ========== Menu Card ========== */
.menu-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.menu-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
}

.card-image-wrapper {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #f8f9fa;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.menu-card:hover .card-image {
  transform: scale(1.08);
}

.price-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 8px 14px;
  border-radius: 20px;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
}

.currency {
  font-size: 0.85rem;
  opacity: 0.9;
}

.category-badge {
  position: absolute;
  bottom: 12px;
  left: 12px;
  background: rgba(255, 255, 255, 0.95);
  color: #495057;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.card-content {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.item-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #212529;
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.item-description {
  color: #6c757d;
  font-size: 0.9rem;
  margin: 0 0 16px 0;
  flex: 1;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.5;
}

/* ========== Card Actions ========== */
.card-actions {
  display: flex;
  gap: 10px;
  align-items: stretch;
  margin-top: auto;
}

.quantity-selector {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  border-radius: 10px;
  overflow: hidden;
}

.qty-btn {
  width: 36px;
  height: 40px;
  border: none;
  background: transparent;
  color: #495057;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
}

.qty-btn:hover:not(:disabled) {
  background: #e9ecef;
  color: #667eea;
}

.qty-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.qty-input {
  width: 45px;
  border: none;
  background: transparent;
  text-align: center;
  font-weight: 600;
  color: #212529;
  font-size: 1rem;
}

.add-btn {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 16px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.add-btn:active {
  transform: translateY(0);
}

/* ========== Empty State ========== */
.empty-state {
  background: white;
  border-radius: 16px;
  padding: 60px 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.empty-icon {
  font-size: 4rem;
  color: #dee2e6;
}

/* ========== Toast ========== */
.toast-success {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  color: white;
}

.toast-error {
  background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);
  color: white;
}

.toast-body {
  padding: 14px 18px;
  font-weight: 500;
}

/* ========== Loading State ========== */
.loading-state {
  background: white;
  border-radius: 16px;
  padding: 60px 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .page-title {
    font-size: 1.8rem;
  }

  .menu-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }

  .card-image-wrapper {
    height: 180px;
  }
}

@media (max-width: 576px) {
  .menu-grid {
    grid-template-columns: 1fr;
  }

  .card-actions {
    flex-direction: column;
  }

  .quantity-selector {
    justify-content: center;
  }
}
</style>