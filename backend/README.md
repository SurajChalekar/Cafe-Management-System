# 🍽️ Cafe Management System – Django Backend

A modern, feature-rich backend API for managing cafe operations, built with Django and Django REST Framework. This system provides comprehensive endpoints for menu management, order processing, authentication, and staff operations.

---

## 🧠 Core Features

### 🛍️ Menu Management
- 📋 **Full CRUD Operations** — Staff can add, edit, and delete menu items
- 🖼️ **Image Upload** — Upload and display images for each menu item
- 🔍 **Advanced Search & Filtering** — Search by name, price, or description
- ✅ **Availability Control** — Mark items as available/unavailable in real-time
- 💾 **Persistent Storage** — Uploaded images are securely stored and served

### 🧾 Ordering System
- 🛒 **Smart Shopping Cart** — Add, remove, and update items with ease
- 💰 **Dynamic Calculations** — Real-time total calculation for items and amounts
- 🚀 **Quick Checkout** — Place orders directly from cart
- 🧹 **Auto Cart Clear** — Cart clears instantly after successful checkout
- 👩‍💼 **Role-Based Endpoints** — Separate APIs for staff and customer operations
- ⚙️ **Global Order Toggle** — Staff can enable/disable ordering system-wide

### 👥 User Roles & Authentication
- 🔐 **JWT Authentication** — Secure login, register, and logout functionality
- 👨‍🍳 **Three-Tier Permissions** — Customer, Staff, and Admin roles
- 👁️ **Staff Dashboard** — Exclusive management interface for staff members
- 🔒 **Token-Based Security** — Protected endpoints with automatic token refresh

### 🎨 Frontend (Vue 3 + Bootstrap)
- 🖼️ **Modern UI/UX** — Beautiful, responsive design that works on all devices
- 🌈 **Themed Interface** — Gradient-styled pages with elegant modals and alerts
- 🧭 **Dynamic Navigation** — Context-aware navigation based on user roles
- 💬 **Real-Time Feedback** — Instant UI updates for all operations (success, error, loading states)
- ⚡ **Smooth Interactions** — Optimized performance with Vue 3 Composition API

### ⚙️ Backend (Django REST Framework)
- 📦 **Clean API Architecture** — RESTful endpoints: `/api/v1/menu/`, `/api/v1/orders/`, `/api/v1/auth/`
- 🔍 **Built-in Filtering** — Search, filter, and ordering capabilities for menu items
- 🧩 **Modular Design** — Organized apps: `menu`, `orders`, `users`
- 🧠 **Class-Based Views** — Efficient DRF views (`ListAPIView`, `RetrieveAPIView`, etc.)
- 🛡️ **Secure & Scalable** — Production-ready architecture with best practices

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.10+ | Core language |
| **Django** | 5.x | Web framework |
| **Django REST Framework** | Latest | API development |
| **Simple JWT** | Latest | Authentication |
| **Django Channels** | Latest | WebSocket support |
| **SQLite / PostgreSQL** | - | Database (configurable) |
| **CORS Headers** | Latest | Cross-origin requests |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment tool

### Installation

**1. Navigate to the backend directory**
```bash
cd backend
```

**2. Create and activate virtual environment**

*Windows:*
```bash
python -m venv venv
venv\Scripts\activate
```

*macOS / Linux:*
```bash
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure database**
```bash
python manage.py migrate
```

**5. Create superuser (optional)**
```bash
python manage.py createsuperuser
```

**6. Launch development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

---

## 📚 API Documentation

Once the server is running, access the interactive API documentation:
- **Browsable API**: `http://localhost:8000/api/`
- **Admin Panel**: `http://localhost:8000/admin/`

---

**Built with ❤️ using Django**
