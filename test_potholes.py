"""
Test file for Potholes router

To run tests:
1. Install pytest: pip install pytest httpx
2. Run: pytest test_potholes.py -v
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_pothole_helper(full_result: bool = False):
    """Helper to create a new pothole"""
    response = client.post(
        "/api/potholes/",
        json={
            "location": "Forbes Ave & Morewood Ave",
            "reported_date": "2025-11-20",
            "severity": "moderate",
            "size_diameter_cm": 45.0,
            "repair_status": "reported",
            "repair_date": None,
            "repair_cost": None,
            "notes": "Large pothole near the crosswalk"
        }
    )
    if full_result:
        return response
    else:
        data = response.json()
        return data["id"]


def test_create_pothole():
    """Test creating a new pothole"""
    response = create_pothole_helper(full_result=True)
    assert response.status_code == 201
    data = response.json()
    assert data["location"] == "Forbes Ave & Morewood Ave"
    assert data["severity"] == "moderate"
    assert "id" in data

def test_list_potholes():
    """Test listing all potholes"""
    response = client.get("/api/potholes/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "potholes" in data
    assert isinstance(data["potholes"], list)
    

def test_get_pothole():
    """Test getting a specific pothole"""
    # First create a pothole
    pothole_id = create_pothole_helper()

    # Then retrieve it
    response = client.get(f"/api/potholes/{pothole_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == pothole_id


def test_update_pothole():
    """Test updating a pothole"""
    # First create a pothole
    pothole_id = create_pothole_helper()

    response = client.put(
        f"/api/potholes/{pothole_id}",
        json={
            "severity": "severe",
            "repair_status": "scheduled",
            "notes": "Scheduled for repair next week"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["severity"] == "severe"
    assert data["repair_status"] == "scheduled"


def test_delete_pothole():
    """Test deleting a pothole"""
    # First create a pothole
    pothole_id = create_pothole_helper()

    # Then delete it
    response = client.delete(f"/api/potholes/{pothole_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/api/potholes/{pothole_id}")
    assert response.status_code == 404


def test_get_nonexistent_pothole():
    """Test getting a pothole that doesn't exist"""
    response = client.get("/api/potholes/99999")
    assert response.status_code == 404


def test_filter_by_severity():
    """Test filtering potholes by severity"""
    create_pothole_helper()
    response = client.get("/api/potholes/?severity=moderate")
    assert response.status_code == 200
    data = response.json()
    assert "potholes" in data


def test_filter_by_repair_status():
    """Test filtering potholes by repair status"""
    create_pothole_helper()
    response = client.get("/api/potholes/?repair_status=reported")
    assert response.status_code == 200
    data = response.json()
    assert "potholes" in data

def test_search_potholes():
    """Test searching potholes by location"""
    create_pothole_helper()
    response = client.get("/api/potholes/?search=Forbes")
    assert response.status_code == 200
    data = response.json()
    assert "potholes" in data


if __name__ == "__main__":
    print("Run with: pytest test_potholes.py -v")
