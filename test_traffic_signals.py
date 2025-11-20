"""
Test file for Traffic Signals router
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def create_traffic_signal_helper(full_result=False):
    """Helper to create a new traffic signal"""
    response = client.post(
        "/api/traffic-signals/",
        json={
            "intersection_name": "Main St & 1st Ave",
            "location": "Downtown",
            "signal_type": "standard",
            "cycle_length_seconds": 120,
            "malfunction_count": 0,
            "has_turn_arrow": True
        }
    )
    if full_result:
        return response
    else:
        data = response.json()
        return data["id"]

def test_create_traffic_signal():
    """Test creating a new traffic signal"""
    response = create_traffic_signal_helper(full_result=True)
    assert response.status_code == 201
    data = response.json()
    assert data["intersection_name"] == "Main St & 1st Ave"
    assert data["signal_type"] == "standard"
    assert "id" in data

def test_list_traffic_signals():
    """Test listing all traffic signals"""
    response = client.get("/api/traffic-signals/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "traffic_signals" in data
    assert isinstance(data["traffic_signals"], list)

def test_get_traffic_signal():
    """Test getting a specific traffic signal"""
    signal_id = create_traffic_signal_helper()
    response = client.get(f"/api/traffic-signals/{signal_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == signal_id

def test_update_traffic_signal():
    """Test updating a traffic signal"""
    signal_id = create_traffic_signal_helper()
    response = client.put(
        f"/api/traffic-signals/{signal_id}",
        json={"cycle_length_seconds": 90}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["cycle_length_seconds"] == 90

def test_delete_traffic_signal():
    """Test deleting a traffic signal"""
    signal_id = create_traffic_signal_helper()
    response = client.delete(f"/api/traffic-signals/{signal_id}")
    assert response.status_code == 204
    response = client.get(f"/api/traffic-signals/{signal_id}")
    assert response.status_code == 404

def test_get_nonexistent_traffic_signal():
    """Test getting a traffic signal that doesn't exist"""
    response = client.get("/api/traffic-signals/99999")
    assert response.status_code == 404

def test_filter_by_signal_type():
    """Test filtering traffic signals by type"""
    response = client.get("/api/traffic-signals/?signal_type=standard")
    assert response.status_code == 200

def test_search_traffic_signals():
    """Test searching traffic signals"""
    response = client.get("/api/traffic-signals/?search=Main")
    assert response.status_code == 200

if __name__ == "__main__":
    print("Run with: pytest test_traffic_signals.py -v")
