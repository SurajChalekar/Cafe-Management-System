<template>
  <div class="orders-container">
    <div class="decor">
      <div class="blob blob-a"></div>
      <div class="blob blob-b"></div>
      <div class="blob blob-c"></div>
    </div>

    <div class="container py-5" style="position: relative; z-index: 10;">
      <div class="text-center mb-5 animate-fade-in">
        <h1 class="display-3 fw-bold text-white mb-3">
          <i class="bi bi-list-check me-3"></i>
          Active Orders
        </h1>
        <p class="lead text-white-50 fs-4">Manage and update order status</p>
      </div>

      <div class="mb-5 text-center">
        <button @click="toggleGlobalOrders"
          :class="['btn', 'btn-lg', 'shadow-lg', 'toggle-btn', 'px-5', 'py-3', 'rounded-pill', allowOrders ? 'btn-danger' : 'btn-success']">
          <i :class="allowOrders ? 'bi bi-x-circle me-2 fs-5' : 'bi bi-check-circle me-2 fs-5'"></i>
          <span class="fs-5 fw-bold">{{ allowOrders ? 'Disable Orders' : 'Enable Orders' }}</span>
        </button>
      </div>

      <div class="row g-4">
        <div v-for="(order, index) in orders" :key="order.id ?? index" class="col-lg-6 col-xl-4">
          <div class="card order-card shadow-lg h-100 border-0" :style="{ animationDelay: `${index * 0.1}s` }">
            <div class="card-header-custom">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <h4 class="mb-1 text-white fw-bold">
                    <i class="bi bi-receipt me-2"></i>
                    Order #{{ order.id ?? 'N/A' }}
                  </h4>
                  <small class="text-white-50 fs-6">
                    <i class="bi bi-clock me-1"></i>
                    {{ formatTime(order.created_at) }}
                  </small>
                </div>
                <span class="badge status-badge fs-6" :class="getStatusBadgeClass(order.status)">
                  <span class="status-dot me-1"></span>
                  {{ formatStatus(order.status) }}
                </span>
              </div>
            </div>

            <div class="card-body p-4">
              <div class="customer-info mb-4 p-3 bg-light rounded-3">
                <div class="d-flex align-items-center">
                  <div class="customer-icon me-3">
                    <i class="bi bi-person-fill"></i>
                  </div>
                  <div>
                    <small class="text-muted d-block fw-semibold">Customer</small>
                    <strong class="fs-5">{{ order.customer_name }}</strong>
                  </div>
                </div>
              </div>

              <h6 class="mb-3 fw-bold text-uppercase text-muted">
                <i class="bi bi-bag me-2 text-primary fs-5"></i>
                Order Items ({{ order.items.length }})
              </h6>

              <ul class="list-unstyled mb-4 order-items-list">
                <li v-for="(item, i) in order.items" :key="i"
                  class="order-item d-flex justify-content-between align-items-center mb-3 p-3 rounded-3">
                  <div class="item-info">
                    <div class="item-name fw-semibold mb-2">
                      {{ item.item_name ?? item.name ?? 'Unknown Item' }}
                    </div>
                    <div class="quantity-badge">
                      <i class="bi bi-x-lg me-1"></i>
                      <span class="fw-bold">{{ item.quantity }}</span>
                    </div>
                  </div>
                  <div class="item-price text-end">
                    <div class="fw-bold text-primary fs-5">
                      ₹{{ (Number(item.price ?? 0) * Number(item.quantity ?? 0)).toFixed(2) }}
                    </div>
                  </div>
                </li>
              </ul>

              <div class="total-box d-flex justify-content-between align-items-center mb-4 p-4 bg-success bg-opacity-10 rounded-3">
                <h5 class="mb-0 fw-bold text-success">
                  <i class="bi bi-cash-stack me-2"></i>Total:
                </h5>
                <h4 class="mb-0 fw-bold text-success">
                  ₹{{ (order.total ?? order.total_price ?? 0).toFixed(2) }}
                </h4>
              </div>

              <div class="status-buttons d-flex gap-2">
                <button class="btn flex-fill py-3 status-btn"
                  :class="order.status === 'preparing' ? 'btn-warning active' : 'btn-outline-warning'"
                  @click="updateStatus(order, 'preparing')" 
                  :disabled="order.status === 'preparing'">
                  <i class="bi bi-clock-history me-2 fs-5"></i>
                  <span class="fw-semibold fs-6">Preparing</span>
                </button>
                <button class="btn flex-fill py-3 status-btn"
                  :class="order.status === 'served' ? 'btn-success active' : 'btn-outline-success'"
                  @click="updateStatus(order, 'served')" 
                  :disabled="order.status === 'served'">
                  <i class="bi bi-check-circle me-2 fs-5"></i>
                  <span class="fw-semibold fs-6">Served</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="orders.length === 0" class="empty-state">
        <div class="card shadow-lg border-0 rounded-4 p-5 mx-auto text-center" style="max-width: 600px;">
          <div class="empty-icon mb-4 mx-auto">
            <i class="bi bi-inbox"></i>
          </div>
          <h3 class="fw-bold mb-3">No Active Orders</h3>
          <p class="text-muted fs-5 mb-0">All orders have been completed!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/axios'

const orders = ref([])
const allowOrders = ref(true)

const getStatusBadgeClass = (status) => {
  switch (status) {
    case 'preparing': return 'bg-warning text-dark'
    case 'served': return 'bg-success text-white'
    case 'pending': return 'bg-secondary text-white'
    default: return 'bg-info text-dark'
  }
}

const formatStatus = (status) => status ? status.charAt(0).toUpperCase() + status.slice(1) : 'Unknown'

const formatTime = (timestamp) => {
  if (!timestamp) return '-'
  const date = new Date(timestamp)
  return date.toLocaleString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

const fetchOrders = async () => {
  try {
    const response = await api.get('orders/orders/active/')
    const data = Array.isArray(response.data) ? response.data : response.data.results ?? []
    console.log('✅ Fetched orders:', data)
    orders.value = data.map(order => ({
      id: order.id,
      status: (order.status ?? 'pending').toLowerCase(),
      created_at: order.created_at,
      total: order.total_price ?? 0,
      customer_name: order.customer ?? 'Unknown',
      items: order.order_items ?? []
    }))
  } catch (error) {
    console.error('❌ Error fetching orders:', error)
    orders.value = []
  }
}

const updateStatus = async (order, newStatus) => {
  try {
    const response = await api.patch(`orders/orders/update/${order.id}/`, { status: newStatus })
    order.status = newStatus
    console.log('✅ Updated:', response.data)
  } catch (error) {
    console.error('❌ Error updating status:', error.response?.data || error)
  }
}

const fetchGlobalOrders = async () => {
  const res = await api.get('orders/staff/global-order-toggle/')
  allowOrders.value = res.data.allow_orders
}

const toggleGlobalOrders = async () => {
  try {
    console.log("Toggling global orders...");
    const res = await api.patch('orders/staff/global-order-toggle/', {
      allow_orders: !allowOrders.value
    });
    console.log("✅ Response:", res.data);
    allowOrders.value = res.data.allow_orders;
  } catch (err) {
    console.error("❌ Error toggling global orders:", err.response?.status, err.response?.data || err);
  }
};

onMounted(() => {
  fetchOrders()
  fetchGlobalOrders()
})
</script>

<style scoped>
.orders-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  padding-bottom: 4rem;
}

/* Decorative blobs */
.decor .blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
  opacity: 0.3;
  animation: float 20s ease-in-out infinite;
}

.blob-a {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #ffd166, #ff9770);
  top: -150px;
  left: -150px;
  animation-delay: 0s;
}

.blob-b {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #ef476f, #ff6b9d);
  right: -120px;
  bottom: -140px;
  animation-delay: 5s;
}

.blob-c {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #06ffa5, #00d4ff);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}

/* Fade in animation */
.animate-fade-in {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Toggle button */
.toggle-btn {
  transition: all 0.3s ease;
  border: none;
  position: relative;
  overflow: hidden;
}

.toggle-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.toggle-btn:hover::before {
  width: 300px;
  height: 300px;
}

.toggle-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25) !important;
}

/* Order cards */
.order-card {
  border-radius: 1.25rem;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  animation: slideUp 0.5s ease-out forwards;
  opacity: 0;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.order-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25) !important;
}

.card-header-custom {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1.5rem;
  position: relative;
}

.card-header-custom::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
  pointer-events: none;
}

/* Status badge */
.status-badge {
  font-weight: 600;
  padding: 0.6rem 1rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  border-radius: 20px;
}

.status-dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  display: inline-block;
  background: currentColor;
  animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Customer info */
.customer-info {
  border: 2px solid #e9ecef;
  transition: all 0.2s ease;
}

.customer-info:hover {
  border-color: #667eea;
  transform: scale(1.02);
}

.customer-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
}


.order-item {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  transition: all 0.2s ease;
}

.order-item:hover {
  background: white;
  border-color: #667eea;
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.item-name {
  color: #2d3748;
  line-height: 1.4;
  font-size: 1.1rem;
}

.quantity-badge {
  display: inline-flex;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.9rem;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.quantity-badge i {
  font-size: 0.7rem;
}

.item-price {
  font-size: 1.1rem;
}

/* Total box */
.total-box {
  border: 2px solid rgba(25, 135, 84, 0.3);
  transition: all 0.2s ease;
}

.total-box:hover {
  border-color: #198754;
  transform: scale(1.03);
  box-shadow: 0 4px 16px rgba(25, 135, 84, 0.2);
}

/* Status buttons */
.status-buttons {
  gap: 0.75rem;
}

.status-btn {
  border-radius: 12px;
  border-width: 2px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.status-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.4s, height 0.4s;
}

.status-btn:hover::before {
  width: 200px;
  height: 200px;
}

.status-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.status-btn.active {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.status-btn:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

/* Empty state */
.empty-state .empty-icon {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3.5rem;
  color: white;
}

/* Responsive */
@media (max-width: 768px) {
  .decor .blob {
    display: none;
  }

  .display-3 {
    font-size: 2rem;
  }

  .status-buttons {
    flex-direction: column;
  }

  .status-btn {
    width: 100%;
  }
}
</style>