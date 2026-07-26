import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_admin_system():
    """Test admin login, analytics, and verifications endpoints"""
    print("Testing admin login...")
    response = client.post("/api/auth/token", json={
        "username": "admin@test.com",
        "password": "password123"
    })
    assert response.status_code == 200, f"Admin login failed: {response.status_code} - {response.text}"
    token = response.json()["access_token"]
    assert token is not None, "Missing access_token"
    print("✅ Admin login successful")

    headers = {"Authorization": f"Bearer {token}"}

    print("Testing admin analytics...")
    analytics_res = client.get("/api/auth/admin/analytics", headers=headers)
    assert analytics_res.status_code == 200, f"Analytics failed: {analytics_res.status_code} - {analytics_res.text}"
    analytics_data = analytics_res.json()
    assert "total_users" in analytics_data
    print("✅ Admin analytics retrieved successfully")

    print("Testing admin pending verifications...")
    verif_res = client.get("/api/auth/admin/pending-verifications", headers=headers)
    assert verif_res.status_code == 200, f"Verifications failed: {verif_res.status_code} - {verif_res.text}"
    assert isinstance(verif_res.json(), list)
    print("✅ Admin verifications retrieved successfully")

def test_restaurant_system():
    """Test restaurant login (should work since verified)"""
    print("Testing restaurant login...")
    response = client.post("/api/auth/token", json={
        "username": "restaurant@test.com",
        "password": "password123"
    })
    assert response.status_code == 200, f"Restaurant login failed: {response.status_code} - {response.text}"
    assert "access_token" in response.json()
    print("✅ Restaurant login successful (verified)")

def test_unverified_hotel_registration_and_approval():
    """Test that a new hotel/restaurant registration cannot log in until approved by admin"""
    # Cleanup existing test hotel user if present
    import asyncio
    from backend.database import get_database
    async def cleanup():
        db = get_database()
        await db.users.delete_one({"email": "grandpalace@hotel.com"})
    asyncio.run(cleanup())

    print("Testing new hotel registration...")
    reg_payload = {
        "name": "Grand Palace Hotel",
        "email": "grandpalace@hotel.com",
        "password": "password123",
        "role": "restaurant"
    }
    reg_res = client.post("/api/auth/register", json=reg_payload)
    assert reg_res.status_code == 200, f"Registration failed: {reg_res.status_code} - {reg_res.text}"
    user_id = reg_res.json().get("_id")

    print("Testing unverified login (should be blocked with 403)...")
    login_res = client.post("/api/auth/token", json={
        "username": "grandpalace@hotel.com",
        "password": "password123"
    })
    assert login_res.status_code == 403, f"Expected 403 Forbidden for unverified login, got {login_res.status_code}"
    print("✅ Unverified login blocked as expected (403 Forbidden)")

    print("Admin approving hotel user...")
    admin_login = client.post("/api/auth/token", json={
        "username": "admin@test.com",
        "password": "password123"
    })
    token = admin_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    if not user_id:
        pending = client.get("/api/auth/admin/pending-verifications", headers=headers).json()
        target = next((u for u in pending if u["email"] == "grandpalace@hotel.com"), None)
        assert target is not None, "Hotel user not found in pending list"
        user_id = target["_id"]

    approve_res = client.post(f"/api/auth/admin/verify-user/{user_id}", headers=headers)
    assert approve_res.status_code == 200, f"Approval failed: {approve_res.status_code} - {approve_res.text}"
    print("✅ Admin successfully approved hotel user")

    print("Testing post-approval login...")
    post_login = client.post("/api/auth/token", json={
        "username": "grandpalace@hotel.com",
        "password": "password123"
    })
    assert post_login.status_code == 200, f"Login after approval failed: {post_login.status_code} - {post_login.text}"
    assert "access_token" in post_login.json()
    print("✅ Approved hotel user logged in successfully!")

if __name__ == "__main__":
    print("🧪 Testing FoodShare Admin System")
    print("=" * 40)
    test_admin_system()
    test_restaurant_system()
    test_unverified_hotel_registration_and_approval()
    print("\n🎉 Testing complete!")
