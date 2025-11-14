"""
Test file for Building Permits router
"""

from fastapi.testclient import TestClient
from main import app
from uuid import uuid4

client = TestClient(app)


def create_permit_helper(permit_number="BP-123456", full_result=False):
    """Helper function to create a new building permit"""
    response = client.post(
        "/api/building-permits/",
        json={
            "permit_number": permit_number,
            "address": "123 Test Street",
            "permit_type": "residential",
            "status": "pending",
            "issue_date": "2024-01-01",
            "expiration_date": "2025-01-01",
            "estimated_cost": 50000.0,
            "notes": "Test permit"
        }
    )
    if full_result:
        return response
    return response.json()["id"]


def test_create_permit():
    """Test creating a building permit"""
    response = create_permit_helper(full_result=True)
    assert response.status_code == 201
    data = response.json()
    assert data["permit_number"] == "BP-123456"
    assert data["address"] == "123 Test Street"
    assert "id" in data


def test_list_permits():
    """Test listing building permits"""
    response = client.get("/api/building-permits/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "permits" in data
    assert isinstance(data["permits"], list)


def test_get_permit():
    """Test getting one specific permit"""
    permit_id = create_permit_helper(permit_number=f"BP-{uuid4().hex[:6]}")
    response = client.get(f"/api/building-permits/{permit_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == permit_id


def test_update_permit():
    """Test updating a building permit"""
    permit_id = create_permit_helper(permit_number=f"BP-{uuid4().hex[:6]}")
    response = client.put(
        f"/api/building-permits/{permit_id}",
        json={"status": "approved"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "approved"


def test_delete_permit():
    """Test deleting a building permit"""
    permit_id = create_permit_helper(permit_number=f"BP-{uuid4().hex[:6]}")

    response = client.delete(f"/api/building-permits/{permit_id}")
    assert response.status_code == 204  # No Content

    # Ensure it's really gone
    response = client.get(f"/api/building-permits/{permit_id}")
    assert response.status_code == 404


def test_get_nonexistent_permit():
    """Test requesting a non-existing permit"""
    response = client.get("/api/building-permits/99999")
    assert response.status_code == 404


def test_filter_by_status():
    """Test the filtering feature: by status"""
    response = client.get("/api/building-permits/?status=pending")
    assert response.status_code == 200


def test_filter_by_type():
    """Test filtering by permit type"""
    response = client.get("/api/building-permits/?permit_type=residential")
    assert response.status_code == 200


def test_search_permits():
    """Test searching permits by permit_number/address"""
    response = client.get("/api/building-permits/?search=BP")
    assert response.status_code == 200


if __name__ == "__main__":
    print("Run with: pytest test_building_permits_example.py -v")
