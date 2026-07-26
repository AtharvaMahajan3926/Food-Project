import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_admin_flow():
    """Test admin login and pending verifications endpoint"""
    print("Testing admin login...")
    response = client.post("/api/auth/token", json={
        "username": "admin@test.com",
        "password": "password123"
    })
    assert response.status_code == 200, f"Admin login failed: {response.status_code} - {response.text}"
    
    data = response.json()
    token = data.get("access_token")
    assert token is not None, "Missing access_token"
    print("✅ Admin login successful")

    print("Testing admin verifications...")
    headers = {"Authorization": f"Bearer {token}"}
    verif_res = client.get("/api/auth/admin/pending-verifications", headers=headers)
    assert verif_res.status_code == 200, f"Admin verifications failed: {verif_res.status_code} - {verif_res.text}"
    verif_data = verif_res.json()
    assert isinstance(verif_data, list)
    print("✅ Admin verifications retrieved successfully")

if __name__ == "__main__":
    print("🧪 Testing FoodShare Admin API URLs")
    print("=" * 40)
    test_admin_flow()
    print("\n🎉 Testing complete!")