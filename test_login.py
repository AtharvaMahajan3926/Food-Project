import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_login():
    """Test login with admin credentials"""
    print("Testing admin login...")
    form_data = {
        'username': 'admin@test.com',
        'password': 'password123'
    }

    response = client.post("/api/auth/token", data=form_data)
    assert response.status_code == 200, f"Login failed: {response.status_code} - {response.text}"

    data = response.json()
    token = data.get('access_token')
    assert token is not None, "access_token missing in response"

    headers = {'Authorization': f'Bearer {token}'}
    me_response = client.get("/api/auth/me", headers=headers)
    assert me_response.status_code == 200, f"/me endpoint failed: {me_response.status_code} - {me_response.text}"

    user_data = me_response.json()
    assert user_data.get("email") == "admin@test.com"
    print("✅ Login & /me endpoint verified!")

if __name__ == "__main__":
    print("🧪 Testing FoodShare Login API")
    print("=" * 40)
    test_login()
    print("🎉 All tests passed successfully!")