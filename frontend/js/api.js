const API_URL = 'http://localhost:8000';

function getToken() {
  return localStorage.getItem('foodshare_token');
}

function setToken(token) {
  localStorage.setItem('foodshare_token', token);
}

function removeToken() {
  localStorage.removeItem('foodshare_token');
}

function getAuthHeaders() {
  const token = getToken();
  if (!token) return {};
  return { 'Authorization': `Bearer ${token}` };
}

async function apiFetch(endpoint, options = {}) {
  const headers = {
    ...options.headers,
    ...getAuthHeaders()
  };
  
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = headers['Content-Type'] || 'application/json';
  } else {
    delete headers['Content-Type']; // Let browser set boundary
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers
  });

  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      removeToken();
      window.location.href = 'login.html';
    }
    let errorData;
    try {
      errorData = await response.json();
    } catch {
      throw new Error(`API Error: ${response.status}`);
    }
    throw new Error(errorData.detail || 'API request failed');
  }

  return response.json();
}
