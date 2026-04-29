let currentRole = 'restaurant';

function selectRole(role, el) {
  currentRole = role;
  document.querySelectorAll('.role-btn').forEach(b => b.classList.remove('active'));
  el.classList.add('active');
  updateDynamicAuthFields();
}

function updateDynamicAuthFields() {
  const lic = document.getElementById('reg-license');
  const ngoLocGroup = document.getElementById('reg-ngo-loc-group');
  const ngoGpsBtn = document.getElementById('reg-ngo-gps-btn');
  const nss = document.getElementById('reg-nss-group');
  
  if(lic) lic.classList.toggle('hidden', currentRole !== 'ngo');
  if(ngoLocGroup) ngoLocGroup.classList.toggle('hidden', currentRole !== 'ngo');
  if(ngoGpsBtn) ngoGpsBtn.classList.toggle('hidden', currentRole !== 'ngo');
  if(nss) nss.classList.toggle('hidden', currentRole !== 'volunteer');
}

function toggleRegisterMode() {
  const login = document.getElementById('login-fields');
  const reg = document.getElementById('register-fields');
  if (login.classList.contains('hidden')) {
    login.classList.remove('hidden');
    reg.classList.add('hidden');
  } else {
    login.classList.add('hidden');
    reg.classList.remove('hidden');
    updateDynamicAuthFields();
  }
}

async function doLogin() {
  const email = document.getElementById('auth-email').value.trim().toLowerCase();
  const password = document.getElementById('auth-pass').value;
  
  if (!email || !password) { showToast('⚠️', 'Email and password required', 'var(--amber)'); return; }

  showToast('🔄', 'Logging in...', 'var(--blue)');

  try {
    let formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const data = await apiFetch('/api/auth/token', {
      method: 'POST',
      body: formData,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    
    setToken(data.access_token);
    window.location.reload(); // common.js will handle redirect
  } catch (error) {
    showToast('❌', error.message, 'var(--red)');
  }
}

async function doRegister() {
  const email = document.getElementById('reg-email').value.trim().toLowerCase();
  const password = document.getElementById('reg-pass').value;
  const name = document.getElementById('reg-name').value;
  const license_no = document.getElementById('reg-license').value;
  const ngo_lat_val = document.getElementById('reg-ngo-lat').value;
  const ngo_lng_val = document.getElementById('reg-ngo-lng').value;
  const ngo_lat = ngo_lat_val ? parseFloat(ngo_lat_val) : null;
  const ngo_lng = ngo_lng_val ? parseFloat(ngo_lng_val) : null;
  const is_nss = document.getElementById('reg-nss')?.checked || false;
  
  if (!email || !password || !name) { showToast('⚠️', 'Please fill required fields.', 'var(--amber)'); return; }

  try {
    const payload = { name, email, password, role: currentRole, license_no, ngo_lat, ngo_lng, is_nss };
    await apiFetch('/api/auth/register', { 
        method: 'POST', body: JSON.stringify(payload) 
    });
    
    document.getElementById('auth-email').value = email;
    document.getElementById('auth-pass').value = password;
    showToast('✅', 'Account created! Logging in...', 'var(--accent)');
    toggleRegisterMode();
    await doLogin();
  } catch (error) {
    showToast('❌', error.message, 'var(--red)');
  }
}

function captureNGOGPS(btn) {
  btn.textContent = 'Locating...';
  btn.disabled = true;
  if(navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((pos) => {
          document.getElementById('reg-ngo-lat').value = pos.coords.latitude.toFixed(6);
          document.getElementById('reg-ngo-lng').value = pos.coords.longitude.toFixed(6);
          btn.textContent = '✅ Location Pinned!';
          btn.style.background = 'var(--accent)';
      }, () => { btn.textContent = '❌ Failed to map'; btn.disabled = false; });
  }
}
