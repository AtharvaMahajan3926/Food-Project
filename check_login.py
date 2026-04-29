import requests

BASE_URL = 'http://localhost:8000'
for email in ['atharv@gmail.com', 'admin@test.com', 'restaurant@test.com']:
    resp = requests.post(f'{BASE_URL}/api/auth/token', data={'username': email, 'password': 'password123'})
    print(email, resp.status_code, resp.text)
