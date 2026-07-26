# 🍱 FoodShare Mumbai - Zero Hunger. Zero Waste.

FoodShare Mumbai is a high-performance, real-time social impact platform connecting surplus food donors (restaurants), receiving non-profits (NGOs), and delivery logistics (volunteers) to eliminate urban food waste.

---

## 🚀 Key Features & Performance Architecture

- **High-Performance Express Frontend Runtime**: Lightweight Node.js Express server with GZip compression and HTTP browser caching.
- **FastAPI Async Backend**: Powered by Python FastAPI, MongoDB index optimizations, and dynamic GZip response compression.
- **Dynamic Environment Binding**: Multi-environment API endpoint support via `/env.js` and `.env`.
- **Role-Based Dashboards**: Tailored UI views for Restaurants, NGOs, Volunteers, Students, and Platform Administrators.
- **Dockerized Multi-Container Support**: Instant deployment via `docker-compose`.

---

## 🛠️ Stack & Infrastructure

- **Frontend**: Vanilla JavaScript (ES6+), Modern CSS3 (Glassmorphism & Glow Effects), Node.js Express server.
- **Backend**: FastAPI, PyMongo / Motor, Pydantic v2, Passlib (BCrypt), Python-JOSE (JWT).
- **Database**: MongoDB with automatic index initialization.
- **Containerization**: Docker & Docker Compose.

---

## 📁 Repository Structure

```text
Food_project/
├── backend/                  # FastAPI Python Service
│   ├── routes/               # API Router Endpoints (Auth, Donations, Stats)
│   ├── database.py           # Async MongoDB connection helper
│   ├── main.py               # FastAPI App entrypoint with CORS & GZip
│   ├── models.py             # Pydantic schemas & data models
│   └── Dockerfile            # Container configuration for backend
├── frontend/                 # Express Frontend Web Server
│   ├── css/                  # CSS tokens, animations & glassmorphic styles
│   ├── html/                 # HTML templates (index, login, ngo, admin, etc.)
│   ├── js/                   # Frontend JS modules (api, auth, common, dashboard)
│   ├── .env                  # Runtime environment variables
│   ├── server.js             # Express runtime server with GZip & route handlers
│   └── Dockerfile            # Container configuration for frontend
├── docker-compose.yml        # Orchestration for MongoDB, Backend, Frontend
├── start-frontend.bat        # Quick launcher script for Windows
├── test_admin.py             # Admin system integration test suite
├── test_api.py               # API route verification suite
└── test_login.py             # Authentication verification suite
```

---

## ⚡ Quick Start

### 1. Run via Docker Compose (Recommended)
```bash
docker-compose up --build
```
Access the application at `http://localhost:3000`.

### 2. Manual Startup

#### Backend Service:
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

#### Frontend Service:
```bash
cd frontend
npm install
npm start
```

---

## 🧪 Testing

Run the automated test suites to verify system health:
```bash
python test_login.py
python test_api.py
python test_admin.py
```
