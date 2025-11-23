
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def create_bike_lane_helper(full_result=False):
    """Helper to create a new bike lane"""
    response = client.post(
        "/api/bike-lanes/",
        json={
            "street_name": "Test Street",
            "start_location": "Location A",
            "end_location": "Location B",
            "length_km": 1.3,
            "lane_type": "protected",
            "surface_condition": "good",
            "incidents_lat_year": 2,
            "last_resurfaced": "2022-05-15"
        }
    )
    if full_result:
        return response
    else:
        print(response)
        data = response.json()
        return data["id"]
    
def test_create_bike_lane():
    """Test creating a new bike lane"""
    response = create_bike_lane_helper(full_result=True)
    assert response.status_code == 201
    data = response.json()
    assert data["street_name"] == "Test Street"
    assert data["start_location"] == "Location A"
    assert "id" in data

def test_list_bike_lanes():
    """Test listing all bike lanes"""
    response = client.get("/api/bike-lanes/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "resources" in data
    assert isinstance(data["resources"], list)

def test_get_bike_lane():
    """Test getting a specific bike lane"""
    # First create a bike lane
    bike_lane_id = create_bike_lane_helper()

    # Then retrieve it
    response = client.get(f"/api/bike-lanes/{bike_lane_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == bike_lane_id

def test_update_bike_lane():
    """Test updating a bike lane"""
    # First create a bike lane
    bike_lane_id = create_bike_lane_helper()

    # Update the bike lane
    response = client.put(
        f"/api/bike-lanes/{bike_lane_id}",
        json={
            "surface_condition": "excellent",
            "incidents_lat_year": 0
        }
    )
    assert response.status_code == 200

    # Retrieve the updated bike lane
    response = client.get(f"/api/bike-lanes/{bike_lane_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["surface_condition"] == "excellent"
    assert data["incidents_lat_year"] == 0

def test_delete_bike_lane():
    """Test deleting a bike lane"""
    # First create a bike lane
    bike_lane_id = create_bike_lane_helper()

    # Then delete it
    response = client.delete(f"/api/bike-lanes/{bike_lane_id}")
    assert response.status_code == 204

    # Verify it's deleted
    response = client.get(f"/api/bike-lanes/{bike_lane_id}")
    assert response.status_code == 404

def test_get_nonexistent_bike_lane():
    """Test getting a bike lane that doesn't exist"""
    response = client.get("/api/bike-lanes/99999")
    assert response.status_code == 404

def test_filter_by_condition():
    """Test filtering bike lanes by surface condition"""
    # Create bike lanes with different conditions
    create_bike_lane_helper()
    create_bike_lane_helper()
    
    response = client.get("/api/bike-lanes/?condition=good")
    assert response.status_code == 200
    data = response.json()
    assert all(lane["surface_condition"] == "good" for lane in data["resources"])

def test_search_bike_lanes():
    create_bike_lane_helper()
    
    response = client.get("/api/bike-lanes/?search=Test")
    assert response.status_code == 200
    data = response.json()
    assert any("Test" in lane["street_name"] for lane in data["resources"])

if __name__ == "__main__":
    print("Run with: pytest test_bike_lanes_example.py -v")