"""
Test file for Bus Stops router
Follows the test_bridges_example.py pattern

To run tests:
1. Install pytest: pip install pytest httpx
2. Run: pytest test_bus_stops.py -v
"""
from fastapi.testclient import TestClient
from main import app
import random

client = TestClient(app)

ids_in_use = []

def create_bus_stop_helper(full_result = False):
    """Helper to create a new bus stop"""
    stop_id = create_random_stop_id()

    response = client.post(
        "/api/bus-stops/",
        json={
            "stop_id": stop_id,
            "location": "Forbes Ave & Morewood Ave",
            "routes_served": "1, 5, 22",
            "has_shelter": True,
            "has_bench": False,
            "has_lighting": True,
            "daily_boardings_avg": 120,
            "last_maintenance": "2024-10-01"
        }
    )
    if full_result:
        return response, stop_id
    else:
        data = response.json()
        return data["id"]
    
def create_random_stop_id():
    stop_id = f"STOP_{random.randint(1000, 9999)}"
    ids_in_use.append(stop_id)
    while stop_id in ids_in_use:    # Need unique stop_id
        stop_id = f"STOP_{random.randint(1000, 9999)}" 

    return stop_id


def test_create_bus_stop():
    """Test creating a new bus stop"""
    response, stop_id = create_bus_stop_helper(full_result=True)
    assert response.status_code == 201
    data = response.json()
    assert data["stop_id"] == stop_id
    assert data["location"] == "Forbes Ave & Morewood Ave"
    assert "id" in data


def test_list_bus_stops():
    """Test listing all bus stops"""
    response = client.get("/api/bus-stops/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "bus_stops" in data
    assert isinstance(data["bus_stops"], list)


def test_get_bus_stop():
    """Test getting a specific bus stop"""
    # First create a bus stop
    id = create_bus_stop_helper()
    print(f"Get id we just made = {id}")

    # Then retrieve it
    response = client.get(f"/api/bus-stops/{id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == id


def test_update_bus_stop():
    """Test updating a bus stop"""
    # First create a bus stop
    id = create_bus_stop_helper()

    # Then update it
    response = client.put(
        f"/api/bus-stops/{id}",
        json={"has_bench": True, "daily_boardings_avg": 150}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["has_bench"] is True
    assert data["daily_boardings_avg"] == 150


def test_delete_bus_stop():
    """Test deleting a bus stop"""
    # First create a bus stop
    id = create_bus_stop_helper()

    # Then delete it
    response = client.delete(f"/api/bus-stops/{id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/api/bus-stops/{id}")
    assert response.status_code == 404


def test_get_nonexistent_bus_stop():
    """Test getting a bus stop that doesn't exist"""
    response = client.get("/api/bus-stops/999")
    assert response.status_code == 404


def test_filter_by_amenities():
    """Test filtering bus stops by amenities"""
    # Ensure at least one bus stop exists with these amenities
    create_bus_stop_helper(full_result=True)

    response = client.get("/api/bus-stops/?has_shelter=true&has_lighting=true")
    assert response.status_code == 200
    data = response.json()
    assert "bus_stops" in data


def test_search_bus_stops():
    """Test searching bus stops"""
    # Ensure at least one bus stop exists
    create_bus_stop_helper(full_result=True)

    response = client.get("/api/bus-stops/?search=Forbes")
    assert response.status_code == 200
    data = response.json()
    assert "bus_stops" in data