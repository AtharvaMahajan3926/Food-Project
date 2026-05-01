# 🍽️ FoodLink: Smart Food Donation & Reward Ecosystem

[![GitHub stars](https://img.shields.io/badge/Status-Concept%20%26%20Early%20Development-blue?style=for-the-badge)](https://github.com/Atharva/FoodLink)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)

**FoodLink** is a technology-driven social impact platform based in **Mumbai, India**, designed to bridge the gap between food waste and food insecurity. By connecting surplus food donors—including restaurants, hotels, and households—with verified NGOs, we aim to build a sustainable redistribution network that promotes **UN SDG 2: Zero Hunger**.

---

## ✨ Features & Ecosystem

### 🍱 For Donors (Restaurants & Individuals)
* **Instant Listing:** Upload food type, quantity, and pickup times seamlessly.
* **Gamified Rewards:** Earn points, badges, and reach the top of the leaderboard for your contributions.
* **Brand Visibility:** Partner restaurants gain visibility through social responsibility.

### 🤝 For NGOs (The Receivers)
* **Smart Matching:** Automated matching with nearby donors using the **Google Maps API**.
* **Efficient Logistics:** Coordinated pickup and drop-off via a hybrid volunteer and paid partner model.
* **Real-time Acceptance:** Review and accept donation requests instantly through the dashboard.

### 👑 For Subscribers
* **Exclusive Discounts:** Monthly tiers (₹49–₹199) unlock off-peak discounts at partner restaurants.
* **Impact Funding:** Subscription fees directly support delivery partner payments and operational costs.

---

## 🛠️ Technical Architecture

### Core Stack
| Layer | Technologies | Role |
| :--- | :--- | :--- |
| **Frontend** | **React / HTML, CSS, JS** | Responsive UI with smooth motion animations. |
| **Backend** | **FastAPI / Node.js** | High-performance handling of donation requests. |
| **Database** | **MongoDB / Firestore** | Scalable storage for user profiles and food logs. |
| **Location** | **Google Maps API** | NGO matching and distance calculation. |
| **Auth** | **JWT / Firebase Auth** | Secure, role-based access control. |

---

## 📂 Project Structure
```text
📦 FoodLink
 ┣ 📂 backend       # FastAPI/Node.js logic and API routes
 ┣ 📂 frontend      # React components and UI motion logic
 ┣ 📜 .env          # API keys for Google Maps & Database
 ┣ 📜 requirements  # Backend dependencies
 ┗ 📜 README.md     # Project documentation
```

---

## 🚀 Future Roadmap
- [ ] **AI Integration:** Demand prediction based on area and time of day.
- [ ] **Mobile App:** Native Android and iOS applications.
- [ ] **Third-Party Logistics:** Integration with platforms like Zomato/Swiggy for last-mile delivery.
- [ ] **National Expansion:** Scaling from Mumbai to other major metro cities.

---

## 🤝 Team & Support
* **Developer:** Atharva Mahajan
* **Target:** Mumbai-based social impact initiatives

> **Impact Dashboard:** FoodLink includes a live counter of meals donated, food saved, and people helped to ensure total transparency.

---

## 🌍 Vision
> “Connecting surplus food with those who need it most, one meal at a time.”
