<template>
  <div class="orders-page">
    <div class="decor">
      <div class="blob blob-a"></div>
      <div class="blob blob-b"></div>
      <div class="blob blob-c"></div>
    </div>

    <div class="container py-5" style="position:relative; z-index:10;">
      <div class="row align-items-center mb-5">
        <div class="col-md-8">
          <h1 class="display-4 fw-bold text-white mb-2 animate-fade-in">My Orders</h1>
          <p class="text-white-50 mb-0 fs-5">Track and manage your past orders and current status.</p>
        </div>
        <div class="col-md-4 text-md-end mt-3 mt-md-0">
          <div class="stats-card bg-white rounded-4 px-4 py-3 d-inline-flex align-items-center shadow-lg">
            <div class="stats-icon me-3">
              <i class="bi bi-bag-check-fill"></i>
            </div>
            <div>
              <small class="d-block text-muted fw-semibold">Total Orders</small>
              <strong class="h4 mb-0 text-primary">{{ orders.length }}</strong>
            </div>
          </div>
        </div>
      </div>

      <div v-if="loading" class="text-center py-5">
        <div class="loading-spinner">
          <div class="spinner-border text-light" role="status" style="width:4rem; height:4rem;"></div>
        </div>
        <p class="text-white mt-4 mb-0 fs-5">Loading your orders…</p>
      </div>

      <div v-else-if="error" class="alert alert-danger shadow-lg border-0 rounded-4 d-flex align-items-center">
        <i class="bi bi-exclamation-triangle-fill me-3 fs-4"></i>
        <div>
          <strong>Error:</strong> {{ error }}
        </div>
      </div>

      <div v-else-if="orders.length === 0" class="empty-state">
        <div class="card shadow-lg border-0 text-center p-5 rounded-4">
          <div class="card-body py-5">
            <div class="empty-icon mb-4">
              <i class="bi bi-bag-x"></i>
            </div>
            <h3 class="mb-3 fw-bold">No orders yet</h3>
            <p class="text-muted mb-4 fs-5">Start shopping and your orders will appear here.</p>
            <router-link to="/menu" class="btn btn-primary btn-lg px-5 rounded-pill shadow-sm">
              <i class="bi bi-card-list me-2"></i> Browse Menu
            </router-link>
          </div>
        </div>
      </div>

      <div v-else class="row g-4">
        <div v-for="(order, i) in orders" :key="order.id" class="col-12 col-md-6 col-xl-4">
          <div class="card order-card h-100 shadow border-0" :style="{ animationDelay: `${i * 0.1}s` }">
            <div class="card-header text-white border-0 order-header">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <small class="text-white-50 d-block mb-1">Order ID</small>
                  <div class="fw-bold fs-5">#{{ order.id }}</div>
                </div>
                <span :class="['badge rounded-pill status-badge', statusBadgeClass(order.status)]">
                  <span class="status-dot me-1"></span>
                  {{ order.status }}
                </span>
              </div>
            </div>

            <div class="card-body p-4">
              <div class="items-header mb-3">
                <i class="bi bi-basket me-2 text-primary fs-5"></i>
                <small class="text-muted text-uppercase fw-semibold fs-6">Items ({{ order.items.length }})</small>
              </div>

              <ul class="list-unstyled mb-3 order-items">
                <li v-for="(it, idx) in order.items" :key="idx" class="order-item d-flex justify-content-between align-items-start mb-3 pb-3">
                  <div class="item-info flex-grow-1 pe-3">
                    <div class="item-name fw-semibold mb-2">{{ it.product_name }}</div>
                    <div class="quantity-badge">
                      <i class="bi bi-x-lg me-1"></i>
                      <span class="fw-bold">{{ it.quantity }}</span>
                    </div>
                  </div>
                  <div class="item-price text-end">
                    <div class="fw-bold text-primary fs-5">₹{{ (it.price * it.quantity).toFixed(2) }}</div>
                    <small class="text-muted fs-6">₹{{ it.price.toFixed(2) }} each</small>
                  </div>
                </li>
              </ul>

              <div class="order-meta row g-2">
                <div class="col-7">
                  <div class="meta-box bg-light rounded-3 p-3 h-100">
                    <i class="bi bi-calendar-event text-primary me-2 fs-5"></i>
                    <small class="text-muted d-block mb-1 fs-6">Placed On</small>
                    <div class="small fw-semibold fs-6">{{ formatDate(order.created_at) }}</div>
                  </div>
                </div>
                <div class="col-5">
                  <div class="meta-box bg-success bg-opacity-10 rounded-3 p-3 h-100 text-center">
                    <small class="text-success d-block mb-1 fw-semibold fs-6">Total</small>
                    <div class="fw-bold text-success fs-4">₹{{ (Number(order.total_price) || 0).toFixed(2) }}</div>
                  </div>
                </div>
              </div>


            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api/axios";

export default {
  name: "CustomerOrders",
  data() {
    return {
      orders: [],
      loading: false,
      error: null,
    };
  },
  methods: {
    async fetchOrders() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get("orders/");
        const raw = Array.isArray(response.data) ? response.data : response.data.results || [];
        this.orders = raw.map(o => ({
          id: o.id,
          total_price: o.total ?? o.total_price ?? 0,
          status: (o.status || "Unknown").toString(),
          created_at: o.created_at || new Date().toISOString(),
          items: Array.isArray(o.order_items)
            ? o.order_items.map(it => ({
              product_name: it.item_name ?? it.product_name ?? it.name ?? "Item",
              quantity: it.quantity ?? 1,
              price: Number(it.price ?? 0)
            }))
            : []
        })).sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      } catch (err) {
        this.error = err.response?.data?.detail || "Failed to load orders.";
      } finally {
        this.loading = false;
      }
    },
    formatDate(s) {
      const d = new Date(s);
      return d.toLocaleString(undefined, { month: "short", day: "numeric", year: "numeric", hour: "2-digit", minute: "2-digit" });
    },
    statusBadgeClass(status) {
      const s = (status || "").toString().toLowerCase();
      if (s.includes("pending")) return "pending";
      if (s.includes("processing")) return "processing";
      if (s.includes("completed") || s.includes("done")) return "completed";
      if (s.includes("cancel") || s.includes("rejected")) return "cancelled";
      return "neutral";
    }
  },
  mounted() {
    this.fetchOrders();
  }
};
</script>

<style scoped>
.orders-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
  padding-bottom: 4rem;
}

/* Decorative blobs with animation */
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

/* Stats card */
.stats-card {
  transition: all 0.3s ease;
  border: 2px solid rgba(102, 126, 234, 0.2);
  backdrop-filter: blur(10px);
}

.stats-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15) !important;
}

.stats-icon {
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

/* Loading spinner */
.loading-spinner {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

/* Empty state */
.empty-state .empty-icon {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 3.5rem;
  color: white;
  margin: 0 auto;
}

/* Order cards */
.order-card {
  border-radius: 1.25rem;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  animation: slideUp 0.5s ease-out forwards;
  opacity: 0;
  backdrop-filter: blur(10px);
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
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2) !important;
}

.order-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1.25rem 1.5rem;
  position: relative;
  overflow: hidden;
}

.order-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
  pointer-events: none;
}

/* Status badges */
.status-badge {
  font-weight: 600;
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.status-badge:hover {
  transform: scale(1.05);
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

.status-badge.pending {
  background: linear-gradient(135deg, #fff3cd, #ffe69c);
  color: #925700;
}

.status-badge.processing {
  background: linear-gradient(135deg, #cff4fc, #9eeaf9);
  color: #055160;
}

.status-badge.completed {
  background: linear-gradient(135deg, #d1fae5, #a7f3d0);
  color: #065f46;
}

.status-badge.cancelled {
  background: linear-gradient(135deg, #ffdede, #ffc0c0);
  color: #7a0b0b;
}

.status-badge.neutral {
  background: linear-gradient(135deg, #e9ecef, #dee2e6);
  color: #495057;
}

/* Items section */
.items-header {
  display: flex;
  align-items: center;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #f0f0f0;
}

.order-item {
  border-bottom: 1px solid #f0f0f0;
  transition: all 0.2s ease;
  padding: 0.75rem;
  margin: 0 -0.75rem;
  border-radius: 0.5rem;
}

.order-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
  margin-bottom: 0;
}

.order-item:hover {
  background: #f8f9fa;
  transform: translateX(4px);
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
  min-width: 90px;
  font-size: 1.1rem;
}

/* Meta boxes */
.meta-box {
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.meta-box:hover {
  border-color: #667eea;
  transform: scale(1.03);
}

/* Button hover effect */
.btn-hover {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.btn-hover::before {
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

.btn-hover:hover::before {
  width: 300px;
  height: 300px;
}

.btn-hover:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
}

/* Responsive */
@media (max-width: 768px) {
  .decor .blob {
    display: none;
  }

  .display-4 {
    font-size: 2rem;
  }

  .stats-card {
    width: 100%;
    justify-content: center;
  }

  .order-card {
    margin-bottom: 1rem;
  }

  .item-name {
    font-size: 0.9rem;
  }
}

@media (max-width: 576px) {
  .order-meta .col-7,
  .order-meta .col-5 {
    flex: 0 0 100%;
    max-width: 100%;
  }
}
</style>