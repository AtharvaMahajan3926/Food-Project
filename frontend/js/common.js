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

let liveCount = 247;
function startLiveCounter() {
  setInterval(() => {
    liveCount += Math.floor(Math.random() * 2);
    const liveCountEl = document.getElementById('live-count');
    if (liveCountEl) {
      liveCountEl.textContent = `${liveCount} meals today`;
    }
  }, 5000);
}

document.addEventListener('DOMContentLoaded', () => {
  checkAuthAndRoute();
  startLiveCounter();
});
