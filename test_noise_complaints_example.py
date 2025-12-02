"""
Example test file for Bridges router
Use this as a reference for testing your own routers

To run tests:
1. Install pytest: pip install pytest httpx
2. Run: pytest test_bridges_example.py -v
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_complaint_helper(full_result=False):
    """Helper to create a new complaint"""
    response = client.post(
        "/api/noise_complaints/",
        json={
            "name": "Weronika Przedworska",
            "location": "Pittsburgh",
            "reported_date": "2025-03-20",
            "time_of_day": "22:30",
            "decibel_level": 67,
            "status": "open",
            "noise_source": "residential",
            "resolution_date": "2025-03-25",
            "notes": "AAAAAAAAAAAAAAAAAAAAAAAAAA"
        }
    )
    if full_result:
        return response
    else:
        data = response.json()
        return data["id"]

def test_create_complaint():
    """Test creating a new complaint"""
    response = create_complaint_helper(full_result=True)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Weronika Przedworska"
    assert data["location"] == "Pittsburgh"
    assert "id" in data

def test_list_complaint():
    """Test listing all complaint"""
    response = client.get("/api/noise_complaints/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "noise_complaints" in data
    assert isinstance(data["noise_complaints"], list)


def test_get_complaint():
    """Test getting a specific complaint"""
    # First create a complaint
    noise_complaint_id = create_complaint_helper()

    # Then retrieve it
    response = client.get(f"/api/noise_complaints/{noise_complaint_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == noise_complaint_id


def test_update_complaint():
    """Test updating a complaint"""
    # First create a complaint
    noise_complaint_id = create_complaint_helper()

    # Then update it
    response = client.put(
        f"/api/noise_complaints/{noise_complaint_id}",
        json={"status": "open"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "open"


def test_delete_complaint():
    """Test deleting a complaint"""
    # First create a complaint
    noise_complaint_id = create_complaint_helper()

    # Then delete it
    response = client.delete(f"/api/noise_complaints/{noise_complaint_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/api/noise_complaints/{noise_complaint_id}")
    assert response.status_code == 404


def test_get_nonexistent_complaint():
    """Test getting a complaint that doesn't exist"""
    response = client.get("/api/noise_complaints/99999")
    assert response.status_code == 404


def test_filter_by_condition():
    """Test filtering complaints by condition"""
    response = client.get("/api/noise_complaints/?status=open")
    assert response.status_code == 200


def test_search_complaints():
    """Test searching complaint"""
    response = client.get("/api/noise_complaints/?search=Test")
    assert response.status_code == 200


if __name__ == "__main__":
    print("Run with: pytest test_noise_complaints_example.py -v")