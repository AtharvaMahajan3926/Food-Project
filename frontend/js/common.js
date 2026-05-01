function showToast(icon, message, color) {
  const container = document.getElementById('toast-container') || createToastContainer();
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.style.borderColor = color;
  toast.innerHTML = `<span style="font-size:1.2rem">${icon}</span> <span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'fadeOut 0.3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

function createToastContainer() {
  const c = document.createElement('div');
  c.id = 'toast-container';
  c.className = 'toast-container';
  document.body.appendChild(c);
  return c;
}

function doLogout() {
  removeToken();
  window.location.href = 'login.html';
}

function checkAuthAndRoute() {
  const path = window.location.pathname;
  const isPublicPage = path.includes('login.html') || path.includes('index.html') || path === '/' || path.endsWith('/html/');

  if (!getToken()) {
    if (!isPublicPage) {
        window.location.href = 'login.html';
    }
  } else {
    // If we have token, get user data and redirect to dashboard if on login/landing
    apiFetch('/api/auth/me')
      .then(user => {
        if (isPublicPage) {
          window.location.href = `${user.role}.html`;
        } else {
          // Verify we are on the right dashboard
          const currentRolePage = window.location.pathname.split('/').pop().split('.')[0];
          if (currentRolePage !== user.role && currentRolePage !== '') {
            window.location.href = `${user.role}.html`;
          }
          // Initialize dashboard UI
          if (typeof initDashboard === 'function') {
            initDashboard(user);
          }
        }
      })
      .catch(() => {
        removeToken();
        if (!window.location.pathname.includes('login.html') && !window.location.pathname.includes('index.html') && window.location.pathname !== '/') {
            window.location.href = 'login.html';
        }
      });
  }
}

async function startLiveCounter() {
  const updateCount = async () => {
    try {
      const impact = await apiFetch('/api/stats/impact');
      const liveCountEl = document.getElementById('live-count');
      if (liveCountEl) {
        liveCountEl.textContent = `${impact.meals_donated} meals served`;
      }
    } catch (e) {
      console.error('Failed to fetch live stats', e);
    }
  };

  // Initial fetch
  await updateCount();

  // Poll every 10 seconds
  setInterval(updateCount, 10000);
}

// ══════════ THEME TOGGLE LOGIC ══════════
function initTheme() {
  const savedTheme = localStorage.getItem('foodshare_theme') || 'dark'; // Default to dark now
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);
}

function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('foodshare_theme', newTheme);
  updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
  const toggleBtn = document.getElementById('themeToggleBtn');
  if (toggleBtn) {
    toggleBtn.innerHTML = theme === 'dark' ? '☀️' : '🌙';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  checkAuthAndRoute();
  startLiveCounter();

  // Attach theme toggle listener if button exists
  const toggleBtn = document.getElementById('themeToggleBtn');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', toggleTheme);
  }

  // Make brand logo clickable to return to landing page
  const brands = document.querySelectorAll('.brand');
  brands.forEach(b => {
    b.addEventListener('click', () => {
      window.location.href = 'index.html';
    });
  });
});
