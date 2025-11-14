from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def create_sidewalk_helper(full_result=False):
    response = client.post(
        "/api/sidewalk/",
        json={
            "name": "Test Sidewalk",
            "location": "Test City",
            "material": "Concrete",
            "width_meters": 3.0,
            "length_meters": 100.0,
            "number": 5,
            "condition": "good",
            "last_inspection_date": "2024-01-01",
            "slope_percent": 12.5,
            "lighting_level": "good"
        }
    )
    if full_result:
        return response
    return response.json()["id"]

def test_create_sidewalk():
    response = create_sidewalk_helper(full_result=True)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Sidewalk"
    assert "id" in data

def test_list_sidewalks():
    response = client.get("/api/sidewalk/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "resources" in data
    assert isinstance(data["resources"], list)

def test_get_sidewalk():
    sidewalk_id = create_sidewalk_helper()
    response = client.get(f"/api/sidewalk/{sidewalk_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sidewalk_id

def test_update_sidewalk():
    sidewalk_id = create_sidewalk_helper()
    response = client.put(f"/api/sidewalk/{sidewalk_id}", json={"material": "Asphalt"})
    assert response.status_code == 200
    data = response.json()
    assert data["material"] == "Asphalt"

def test_delete_sidewalk():
    sidewalk_id = create_sidewalk_helper()
    response = client.delete(f"/api/sidewalk/{sidewalk_id}")
    assert response.status_code == 204
    response = client.get(f"/api/sidewalk/{sidewalk_id}")
    assert response.status_code == 404
