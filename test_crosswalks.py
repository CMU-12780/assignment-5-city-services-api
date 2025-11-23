from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def create_crosswalk_helper(full_result=False):
    # Creates a new crosswalk
    response = client.post(
        "/api/crosswalks/",
        json={
            "name": "Test Crosswalk",
            "location": "5th Ave and Morewood Ave",
            "width_meters": 3.5,
            "condition": "Good",
            "year_created": "2023",
            "last_inspection_date": "2024-01-15"
        }
    )
    if full_result:
        return response
    else:
        data = response.json()
        return data["id"]

def test_create_crosswalk():
    response = create_crosswalk_helper(full_result=True)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Crosswalk"
    assert data["width_meters"] == 3.5
    assert "id" in data

def test_list_crosswalks():
    create_crosswalk_helper()
    
    response = client.get("/api/crosswalks/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "crosswalks" in data 
    assert isinstance(data["crosswalks"], list)

def test_get_crosswalk():

    crosswalk_id = create_crosswalk_helper()

    # Retrieve the created crosswalk
    response = client.get(f"/api/crosswalks/{crosswalk_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == crosswalk_id
    assert data["name"] == "Test Crosswalk"

def test_update_crosswalk():
    crosswalk_id = create_crosswalk_helper()

    # Update created crosswalk
    response = client.put(
        f"/api/crosswalks/{crosswalk_id}",
        json={
            "condition": "Poor",
            "width_meters": 4.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["condition"] == "Poor"
    assert data["width_meters"] == 4.0

    assert data["name"] == "Test Crosswalk"

def test_delete_crosswalk():
    crosswalk_id = create_crosswalk_helper()

    # Then delete created crosswalk
    response = client.delete(f"/api/crosswalks/{crosswalk_id}")
    assert response.status_code == 204

    # Check that it's gone
    response = client.get(f"/api/crosswalks/{crosswalk_id}")
    assert response.status_code == 404

def test_get_nonexistent_crosswalk():
    """Test getting a crosswalk that doesn't exist"""
    response = client.get("/api/crosswalks/99999")
    assert response.status_code == 404

if __name__ == "__main__":
    print("Run with: pytest test_crosswalks.py -v")