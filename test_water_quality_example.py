"""
Example test file for Water Quality router

To run tests:
1. Install pytest and httpx if needed: pip install pytest httpx
2. Run: pytest test_water_quality_example.py -v
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_sample_helper(full_result=False):
    response = client.post(
        "/api/water-quality/",
        json={
            "site_name": "Test Site",
            "location": "Test Location",
            "sample_date": "2025-11-19",
            "ph": 7.0,
            "turbidity_ntu": 2.5,
            "dissolved_oxygen_mg_l": 7.8,
            "nitrates_mg_l": 0.3,
            "e_coli_count": 5,
            "status": "good",
        },
    )
    if full_result:
        return response
    return response.json()["id"]


def test_create_sample():
    resp = create_sample_helper(full_result=True)
    assert resp.status_code == 201
    data = resp.json()
    assert data["site_name"] == "Test Site"
    assert "id" in data


def test_list_samples():
    resp = client.get("/api/water-quality/")
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data and "samples" in data
    assert isinstance(data["samples"], list)


def test_get_sample():
    sample_id = create_sample_helper()
    resp = client.get(f"/api/water-quality/{sample_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == sample_id


def test_update_sample():
    sample_id = create_sample_helper()
    resp = client.put(f"/api/water-quality/{sample_id}", json={"status": "fair"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "fair"


def test_delete_sample():
    sample_id = create_sample_helper()
    resp = client.delete(f"/api/water-quality/{sample_id}")
    assert resp.status_code == 204
    # verify gone
    resp = client.get(f"/api/water-quality/{sample_id}")
    assert resp.status_code == 404


def test_get_nonexistent_sample():
    resp = client.get("/api/water-quality/999999")
    assert resp.status_code == 404


if __name__ == "__main__":
    print("Run with: pytest test_water_quality_example.py -v")
