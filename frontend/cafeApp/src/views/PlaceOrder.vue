<template>
  <div class="order-container py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div v-if="!allowOrders" class="alert alert-warning text-center fw-semibold shadow-sm mb-4">
          ⚠️ Ordering is currently disabled by the staff. You can still view your past orders.
        </div>

        <div v-else class="alert alert-success text-center fw-semibold shadow-sm mb-4">
          ✅ Ordering is currently open! You can place new orders from the menu.
        </div>

        <div class="col-lg-8">
          <div class="card shadow-lg border-0 rounded-4">
            <div class="card-header bg-primary text-white py-3">
              <h3 class="mb-0">
                <i class="bi bi-cart-check me-2"></i>
                Place Your Order
              </h3>
            </div>

            <div class="card-body p-4">
              <!-- Empty Cart Message -->
              <div v-if="cartItems === null" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>

              <div v-else-if="cartItems.length === 0" class="text-center py-5" >
                <i class="bi bi-cart-x display-1 text-muted mb-3"></i>
                <h4 class="text-muted">Your cart is empty</h4>
                <router-link to="/menu" class="btn btn-primary custom-btn mt-3">
                  <i class="bi bi-card-list me-2"></i>
                  View Menu
                </router-link>
              </div>

              <!-- Cart Items -->
              <div v-else>
                <div class="table-responsive">
                  <table class="table table-hover">
                    <thead class="table-light">
                      <tr>
                        <th>Item</th>
                        <th>Price</th>
                        <th>Quantity</th>
                        <th>Subtotal</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in cartItems" :key="item.id">
                        <td>
                          <!-- Show image if available -->
                          <img v-if="item.image" :src="item.image" alt="item.name" class="me-2 rounded" width="40"
                            height="40" />
                          <strong>{{ item.name || 'Unnamed Item' }}</strong>
                        </td>

                        <!-- Safe price display -->
                        <td>₹{{ (Number(item.price) || 0).toFixed(2) }}</td>

                        <td>
                          <div class="btn-group" role="group">
                            <button class="btn btn-sm btn-outline-secondary" @click="decreaseQuantity(item)">
                              <i class="bi bi-dash"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-secondary" disabled>
                              {{ item.quantity || 0 }}
                            </button>
                            <button class="btn btn-sm btn-outline-secondary" @click="increaseQuantity(item)">
                              <i class="bi bi-plus"></i>
                            </button>
                          </div>
                        </td>

                        <!-- Safe subtotal calculation -->
                        <td>
                          <strong>₹{{ ((Number(item.price) || 0) * (Number(item.quantity) || 0)).toFixed(2) }}</strong>
                        </td>

                        <td>
                          <button class="btn btn-sm btn-danger" @click="removeItem(item)">
                            <i class="bi bi-trash"></i>
                          </button>
                        </td>
                      </tr>

                    </tbody>
                  </table>
                </div>


                <!-- Order Summary -->
                <div class="mt-4 p-4 bg-success bg-opacity-10 rounded">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <h5 class="mb-0">Total Items:</h5>
                    <h5 class="mb-0">{{ totalItems }}</h5>
                  </div>
                  <div class="d-flex justify-content-between align-items-center">
                    <h4 class="mb-0 fw-bold">Total Amount:</h4>
                    <h4 class="mb-0 fw-bold text-success">₹{{ totalAmount.toFixed(2) }}</h4>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="mt-4 d-flex gap-3">
                  <button class="btn btn-success btn-lg flex-grow-1" @click="placeOrder">
                    <i class="bi bi-check-circle me-2"></i>
                    Place Order
                  </button>
                  <button class="btn btn-outline-danger btn-lg" @click="clearCart">
                    <i class="bi bi-x-circle me-2"></i>
                    Clear Cart
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Modal -->
    <div v-if="showSuccessModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="text-center">
          <i class="bi bi-check-circle-fill text-success display-1 mb-3"></i>
          <h3 class="fw-bold mb-3">Order Placed Successfully!</h3>
          <p class="text-muted">Your order has been sent to the kitchen.</p>
          <p class="mb-4"><strong>Order #{{ lastOrderId }}</strong></p>
          <button class="btn btn-primary" @click="closeModal">
            Continue Shopping
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import api from '../api/axios'

const router = useRouter()
const authStore = useAuthStore()
const allowOrders = ref(true) // default true

const cartItems = ref(null)
const showSuccessModal = ref(false)
const lastOrderId = ref(null)

const orderDetails = ref({
  customerName: authStore.userName,
  tableNumber: null,
  notes: ''
})

// Computed totals
const totalItems = computed(() => cartItems.value?.reduce((sum, item) => sum + Number(item.quantity || 0), 0) || 0)
const totalAmount = computed(() => cartItems.value?.reduce((sum, item) => sum + (Number(item.price || 0) * Number(item.quantity || 0)), 0) || 0)
const fetchGlobalOrderStatus = async () => {
  try {
    const res = await api.get('orders/global-order-status/')
    allowOrders.value = res.data.allow_orders
  } catch (err) {
    console.error('Failed to fetch global order status:', err.response?.data || err)
    allowOrders.value = true // fallback
  }
}

// Load cart
const loadCart = async () => {
  try {
    const res = await api.get('orders/cart/')
    const items = Array.isArray(res.data.items) ? res.data.items : []
    cartItems.value = items.map(item => ({
      cartItemId: item.id,        // CartItem ID for backend
      itemId: item.item_id,       // MenuItem ID
      name: item.item_name || 'Unnamed Item',
      price: Number(item.price || 0),
      quantity: Number(item.quantity || 1),
      image: item.image || ''
    }))
  } catch (err) {
    console.error('Failed to load cart:', err)
    cartItems.value = []
  }
}

// Increase quantity
const increaseQuantity = async (cartItem) => {
  if (!cartItem.itemId) return
  try {
    await api.post('orders/cart/add/', { item: cartItem.itemId, quantity: 1 })
    await loadCart()
  } catch (err) {
    console.error('Failed to increase quantity:', err.response?.data || err)
  }
}

// Decrease quantity or remove item
// Decrease quantity by 1
const decreaseQuantity = async (cartItem) => {
  if (!cartItem.cartItemId) return;

  // if quantity is 1, remove item
  if (cartItem.quantity <= 1) {
    await removeItem(cartItem);
    return;
  }

  // Backend does NOT have PUT /cart/add/<id>/, so we must remove and re-add
  try {
    // 1️⃣ Remove the item
    await api.delete(`orders/cart/remove/${cartItem.cartItemId}/`);

    // Reload cart
    await loadCart();
  } catch (err) {
    console.error('Failed to decrease quantity:', err.response?.data || err);
  }
};

// Remove item entirely
const removeItem = async (cartItem) => {
  if (!cartItem.cartItemId) return
  try {
    await api.delete(`orders/cart/remove/${cartItem.cartItemId}/`)
    cartItems.value = cartItems.value.filter(i => i.cartItemId !== cartItem.cartItemId)
  } catch (err) {
    console.error('Failed to remove item:', err.response?.data || err)
  }
}

// Clear entire cart
const clearCart = async () => {
  try {
    await api.delete('orders/cart/clear/')
    cartItems.value = []
  } catch (err) {
    console.error('Failed to clear cart:', err.response?.data || err)
  }
}

const paymentSuccess = async (paymentDetails) => {
  try {
    console.log("Payment successful:", paymentDetails);

    // ✅ Step 1: Verify payment on your backend
    const verifyResponse = await api.post("payments/verify-payment/", {
      razorpay_order_id: paymentDetails.razorpay_order_id,
      razorpay_payment_id: paymentDetails.razorpay_payment_id,
      razorpay_signature: paymentDetails.razorpay_signature,
    });

    console.log("Payment verification response:", verifyResponse.data);

    if (verifyResponse.status === 200) {
      // ✅ Step 2: Once verified, place the order
      const orderRes = await api.post("orders/cart/checkout/", {
        customerName: orderDetails.value.customerName,
        tableNumber: orderDetails.value.tableNumber,
        notes: orderDetails.value.notes,
        total: totalAmount.value,
        items: cartItems.value.map((i) => ({
          product: i.itemId,
          quantity: i.quantity,
        })),
      });

      lastOrderId.value = orderRes.data.id;
      showSuccessModal.value = true;

      // ✅ Step 3: Clear the cart
      await api.delete("orders/cart/clear/");
      cartItems.value = [];
      orderDetails.value = {
        customerName: authStore.userName,
        tableNumber: null,
        notes: "",
      };

      console.log("Order placed successfully:", orderRes.data);
    } else {
      alert("Payment verification failed. Please contact support.");
    }
  } catch (err) {
    console.error("Failed to handle payment success:", err.response?.data || err);
    alert("Payment failed or could not be verified.");
  }
};


// Place order
const placeOrder = async () => {
  if (!allowOrders.value) {
    alert("Ordering is currently disabled by staff.");
    return;
  }

  try {
    // ✅ Step 1: Create Razorpay order
    const res = await api.post("payments/create-order/", { amount: totalAmount.value });
    const { order_id, key, amount, currency } = res.data;

    // ✅ Step 2: Initialize Razorpay
    const options = {
      key: key,
      amount: amount * 100, // amount in paise
      currency: currency,
      name: "Cafe Management System",
      description: "Order Payment",
      order_id: order_id,
      handler: async function (response) {
        // ✅ Step 3: If payment succeeds, verify and place order
        await paymentSuccess(response);
      },
      prefill: {
        name: authStore.userName,
        email: authStore.userEmail,
      },
      theme: { color: "#3399cc" },
    };

    const rzp = new window.Razorpay(options);
    rzp.open();
  } catch (err) {
    console.error("Payment initiation failed:", err.response?.data || err);
    alert("Failed to initiate payment. Please try again.");
  }
};

const closeModal = () => {
  showSuccessModal.value = false
  router.push('/menu')
}
onMounted(() => {
  loadCart()
  fetchGlobalOrderStatus()
})

</script>

<style scoped>
.order-container {
  min-height: 100vh;
  background: #16171f;
}

.card {
  background: rgba(255, 255, 255, 0.95);
}

.card-header {  
  background: #424242 !important;
}

.btn-primary {
  background: #424242;
  border: none;
}
.btn-primary:hover {
  background-color: #4f545a; /* new hover color */
  border-color: #51555a;
  transform: scale(1.05); /* optional hover zoom effect */
}
.custom-btn.router-link-active {
  background-color: #343a40; /* darker pressed color */
  border-color: #343a40;
  transform: scale(0.97); /* slight press-in effect */
  box-shadow: 0 0 0 0.2rem rgba(52, 58, 64, 0.25);
}
.custom-btn {
  background-color: #555c67; /* normal state */
  border-color: #3e4248;
  transition: background-color 0.25s ease, transform 0.15s ease;
}
.custom-btn:active {
  background: linear-gradient(135deg, #2b3035 0%, #1d2125 100%);
  transform: scale(0.95);
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal-content {
  background: white;
  padding: 3rem;
  border-radius: 20px;
  max-width: 500px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.table-hover tbody tr:hover {
  background-color: rgba(102, 126, 234, 0.1);
}
</style>
