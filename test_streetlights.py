"""
Test file for Streetlights router

To run tests:
1. Install pytest: pip install pytest httpx
2. Run: pytest test_streetlights.py -v
"""
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4

client = TestClient(app)


def create_streetlight_helper(full_result=False):
    """Helper to create a new streetlight"""
    pole_id = f"SL-{uuid4()}"
    response = client.post(
        "/api/streetlights/",
        json={
            "location": "Test Street & 1st Ave",
            "pole_id": pole_id,
            "light_type": "LED",
            "wattage": 150,
            "installation_date": "2023-01-01",
            "last_maintenance": "2024-01-01",
            "is_operational": True,
            "energy_consumption_kwh": 100.5
        }
    )
    if full_result:
        return response, pole_id
    else:
        data = response.json()
        return data["id"]

def test_create_streetlight():
    """Test creating a new streetlight"""
    response, pole_id = create_streetlight_helper(full_result=True)
    assert response.status_code == 201
    data = response.json()
    assert data["location"] == "Test Street & 1st Ave"
    assert data["pole_id"] == pole_id
    assert "id" in data

def test_list_streetlights():
    """Test listing all streetlights"""
    response = client.get("/api/streetlights/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "streetlights" in data
    assert isinstance(data["streetlights"], list)


def test_get_streetlight():
    """Test getting a specific streetlight"""
    # First create a streetlight
    streetlight_id = create_streetlight_helper()

    # Then retrieve it
    response = client.get(f"/api/streetlights/{streetlight_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == streetlight_id


def test_update_streetlight():
    """Test updating a streetlight"""
    # First create a streetlight
    streetlight_id = create_streetlight_helper()

    # Then update it
    response = client.put(
        f"/api/streetlights/{streetlight_id}",
        json={"is_operational": False}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_operational"] is False


def test_delete_streetlight():
    """Test deleting a streetlight"""
    # First create a streetlight
    streetlight_id = create_streetlight_helper()

    # Then delete it
    response = client.delete(f"/api/streetlights/{streetlight_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/api/streetlights/{streetlight_id}")
    assert response.status_code == 404


def test_get_nonexistent_streetlight():
    """Test getting a streetlight that doesn't exist"""
    response = client.get("/api/streetlights/99999")
    assert response.status_code == 404


def test_filter_by_light_type():
    """Test filtering streetlights by light type"""
    response = client.get("/api/streetlights/?light_type=LED")
    assert response.status_code == 200


def test_search_streetlights():
    """Test searching streetlights"""
    response = client.get("/api/streetlights/?search=Test")
    assert response.status_code == 200


if __name__ == "__main__":
    print("Run with: pytest test_streetlights_example.py -v")
