// Shared logic for all dashboards

function initDashboard(user) {
  // Update user profile info in sidebar
  const avatar = document.getElementById('user-avatar');
  if (avatar) {
    avatar.textContent = user.name ? user.name[0].toUpperCase() : 'U';
  }
  
  const nameEl = document.getElementById('user-name');
  if (nameEl) {
    nameEl.textContent = user.name;
  }
  
  const roleEl = document.getElementById('user-role-label');
  if (roleEl) {
    roleEl.textContent = user.role.toUpperCase();
  }

  // Set up active state in sidebar navigation
  const currentPage = window.location.pathname.split('/').pop();
  document.querySelectorAll('.nav-item').forEach(el => {
    if (el.getAttribute('href') === currentPage) {
      el.classList.add('active');
    }
  });

  // Load specific page data if function exists
  if (typeof loadDashboardData === 'function') {
    loadDashboardData(user);
  }
}

// Reusable functions for rendering
function renderStatCard(title, value, icon) {
  return `
    <div class="stat-card">
      <div class="stat-icon">${icon}</div>
      <div class="stat-info">
        <h3>${value}</h3>
        <p>${title}</p>
      </div>
    </div>
  `;
}

function renderDonationItem(donation, showActions = false, role = '') {
  const isPending = donation.status === 'pending';
  const isAccepted = donation.status === 'accepted';
  const badgeClass = isPending ? 'pending' : (isAccepted ? 'accepted' : 'delivered');
  
  let actionHtml = '';
  if (showActions) {
    if (role === 'ngo' && isPending) {
      actionHtml = `<button class="btn btn-primary btn-sm" onclick="handleAction('accept', '${donation._id}')">Accept</button>`;
    } else if (role === 'volunteer' && isAccepted && !donation.volunteer_id) {
      actionHtml = `<button class="btn btn-secondary btn-sm" onclick="handleAction('claim', '${donation._id}', ${donation.lat}, ${donation.lng})">Claim Delivery</button>`;
    } else if (role === 'restaurant' && (isPending || isAccepted)) {
      actionHtml = `<button class="btn btn-secondary btn-sm" onclick="handleAction('complete', '${donation._id}')">Mark Complete</button>`;
    }
  }

  return `
    <div class="list-item">
      <div class="item-main">
        <div class="item-icon">🍲</div>
        <div class="item-details">
          <h4>${donation.food_name} <span class="badge ${badgeClass}">${donation.status}</span></h4>
          <div class="item-meta">
            <span>📅 ${donation.date}</span>
            <span>📍 ${donation.location}</span>
            <span>⏱️ Expires: ${donation.expiry_time}</span>
          </div>
        </div>
      </div>
      ${actionHtml ? `<div class="item-actions">${actionHtml}</div>` : ''}
    </div>
  `;
}

async function handleAction(action, id, lat, lng) {
  try {
    await apiFetch(`/api/donations/${id}/${action}`, { method: 'PUT' });
    showToast('✅', `Successfully processed ${action}!`, 'var(--accent)');
    
    if (action === 'claim' && lat && lng) {
      window.open(`https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`, '_blank');
    }
    
    // Reload dashboard data
    setTimeout(() => { window.location.reload(); }, 1000);
  } catch (e) {
    showToast('❌', e.message, 'var(--red)');
  }
}


// ══════════════ TAB SWITCHING ══════════════
function switchTab(viewId, el) {
  // Update sidebar active class
  const sidebarNav = el.closest('.sidebar-nav');
  if (sidebarNav) {
    sidebarNav.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
    el.classList.add('active');
  }
  
  // Hide all sections
  document.querySelectorAll('.dashboard-view').forEach(sec => sec.classList.add('hidden'));
  
  // Show target section
  const target = document.getElementById(viewId);
  if (target) {
    target.classList.remove('hidden');
    // Trigger map resize if map is in this view
    if (viewId === 'view-map' && window.mapInstance) {
      setTimeout(() => window.mapInstance.invalidateSize(), 100);
    }
  }
}

// ══════════════ MAP LOGIC ══════════════
function initMap(mapId) {
  if (!document.getElementById(mapId)) return null;
  if (window.mapInstance) return window.mapInstance;
  
  // Need to make sure L (Leaflet) is loaded in the HTML
  if (typeof L === 'undefined') return null;

  const map = L.map(mapId).setView([19.0760, 72.8777], 11);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap &copy; CARTO'
  }).addTo(map);
  
  window.mapInstance = map;
  return map;
}

function updateMapMarkers(donations) {
  if (!window.mapInstance) return;
  
  // Clear old markers if any (simple implementation)
  if (window.mapMarkers) {
    window.mapMarkers.forEach(m => m.remove());
  }
  window.mapMarkers = [];
  
  donations.forEach(d => {
    if (d.lat && d.lng) {
      let color = d.status === 'pending' ? '#F97316' : '#10B981';
      const markerHtml = `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 3px solid #1B110D; box-shadow: 0 0 10px ${color};"></div>`;
      const icon = L.divIcon({ html: markerHtml, className: 'custom-map-marker', iconSize: [20, 20], iconAnchor: [10, 10] });
      const marker = L.marker([d.lat, d.lng], { icon }).addTo(window.mapInstance);
      marker.bindPopup(`<b>${d.food_name}</b><br>${d.quantity}<br>${d.status}`);
      window.mapMarkers.push(marker);
    }
  });
}

// ══════════════ FORM SUBMISSION ══════════════
async function submitDonation(event) {
  event.preventDefault();
  const form = event.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  
  // Set random lat/lng in Mumbai for demo purposes
  data.lat = 19.0760 + (Math.random() - 0.5) * 0.1;
  data.lng = 72.8777 + (Math.random() - 0.5) * 0.1;

  showToast('🔄', 'Submitting...', 'var(--blue)');
  try {
    await apiFetch('/api/donations', {
      method: 'POST',
      body: JSON.stringify(data)
    });
    showToast('✅', 'Donation Listed Successfully!', 'var(--green)');
    form.reset();
    setTimeout(() => window.location.reload(), 1500);
  } catch (error) {
    showToast('❌', error.message, 'var(--red)');
  }
}
