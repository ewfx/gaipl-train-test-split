# filepath: c:\Users\Admin\Desktop\dashui-synapse-connector\test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_related_incidents():
    incident_number = "INC0000060"
    response = client.get(f"/incident/{incident_number}/related")
    assert response.status_code == 200
    assert "related_incidents" in response.json()
    assert isinstance(response.json()["related_incidents"], list)