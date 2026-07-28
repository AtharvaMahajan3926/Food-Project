<div align="center">

# 🍱 FoodShare Mumbai

### *Zero Hunger. Zero Waste. Zero Excuses.*

**Every night, Mumbai's restaurants throw away food that could feed thousands.
Every night, NGOs across the city scramble to find meals for people who need them.
FoodShare Mumbai closes that gap — in real time.**

[![Made with FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Node.js](https://img.shields.io/badge/Frontend-Node.js-339933?style=for-the-badge&logo=node.js)](https://nodejs.org/)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB-47A248?style=for-the-badge&logo=mongodb)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Deploy-Docker-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)

</div>

---

## 🌆 The Problem We're Solving

Mumbai generates surplus food every single day — from wedding halls to five-star kitchens to your neighborhood *tiffin* service. Meanwhile, NGOs feeding the city's homeless and underprivileged communities operate on tight timelines and tighter budgets. The missing piece was never *goodwill* — it was **coordination**.

FoodShare Mumbai is the coordination layer: a live, three-sided marketplace connecting **donors**, **NGOs**, and **volunteers**, engineered to move food from "about to be wasted" to "someone's dinner" as fast as possible.

---

## 🚀 What Makes It Fast

| Feature | Why It Matters |
|---|---|
| ⚡ **Express Frontend Runtime** | GZip compression + HTTP caching means dashboards load instantly, even on patchy mobile data — critical for volunteers on the move. |
| 🐍 **FastAPI Async Backend** | Non-blocking I/O handles concurrent donation postings and claims without breaking a sweat. |
| 🗂️ **MongoDB Index Optimization** | Sub-second queries even as donation history grows into the thousands. |
| 🌐 **Dynamic Environment Binding** | One codebase, any environment — `/env.js` + `.env` handle local, staging, and production seamlessly. |
| 🎭 **Role-Based Dashboards** | Restaurants, NGOs, Volunteers, Students, and Admins each get a purpose-built view — no clutter, no confusion. |
| 🐳 **One-Command Deployment** | `docker-compose up` and you're live. No "works on my machine" drama. |

---

## 🧩 How It Works

```
🍽️  Restaurant posts surplus food
        │
        ▼
📢  NGO sees it live on their dashboard
        │
        ▼
🙋  Volunteer claims the pickup
        │
        ▼
🚴  Food delivered → Waste avoided → Meals served
```

Every step is logged, timestamped, and visible in real time — so donors know their food didn't go to a landfill, and NGOs know exactly what's coming and when.

---

## 🛠️ Tech Stack

**Frontend** — Vanilla JS (ES6+) for zero-bloat speed, Glassmorphism + glow-effect CSS3 for a UI that feels modern without a heavy framework tax, served via a lean Node.js Express layer.

**Backend** — FastAPI + Pydantic v2 for airtight data validation, PyMongo/Motor for async Mongo access, Passlib (BCrypt) + python-jose (JWT) for security that doesn't cut corners.

**Infrastructure** — MongoDB with automatic index initialization, fully Dockerized for one-command spin-up anywhere.

---

## 📁 Repository Structure

```text
Food_project/
├── backend/                  # FastAPI Python Service
│   ├── routes/                # Auth, Donations, Stats endpoints
│   ├── database.py            # Async MongoDB connection helper
│   ├── main.py                 # FastAPI entrypoint — CORS & GZip configured
│   ├── models.py               # Pydantic schemas & data models
│   └── Dockerfile
├── frontend/                  # Express Frontend Web Server
│   ├── css/                    # Tokens, animations, glassmorphic styles
│   ├── html/                   # index, login, ngo, admin, etc.
│   ├── js/                     # api, auth, common, dashboard modules
│   ├── .env
│   ├── server.js               # Express runtime — GZip & route handlers
│   └── Dockerfile
├── docker-compose.yml         # Orchestrates MongoDB, Backend, Frontend
├── start-frontend.bat         # One-click launcher for Windows
├── test_admin.py               # Admin system integration tests
├── test_api.py                  # API route verification tests
└── test_login.py                # Auth verification tests
```

---

## ⚡ Quick Start

### 🐳 Option 1: Docker Compose *(Recommended)*

```bash
docker-compose up --build
```

Then open **http://localhost:3000** — and watch surplus food find a home.

### 🔧 Option 2: Manual Startup

**Backend:**
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

---

## 🧪 Testing

Run the full verification suite before every deploy:

```bash
python test_login.py     # 🔐 Auth flows
python test_api.py        # 🔌 API routes
python test_admin.py       # 🛡️ Admin system
```

---

<div align="center">

### 💚 Built for a city that never stops eating — and shouldn't have to see food go to waste either.

**Have surplus food? Need surplus food? FoodShare Mumbai has you covered.**

</div>
