import pytest
import sys
import os
import json

# Add the webapp folder to the system path so we can import 'app'
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'webapp'))

from app import app

@pytest.fixture
def client():
    # Configure Flask for testing mode
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_prediction_endpoint(client):
    """
    Test that the /predict endpoint:
    1. Accepts POST requests with JSON.
    2. Returns a valid JSON response.
    3. The response contains the 'positive' key.
    4. Crucial: The value is a BOOLEAN, not a String.
    """
    # Sample input: A clear positive sentence
    payload = ["MLOps is critical for robustness"]
    
    response = client.post('/predict', json=payload)
    
    # 1. Check Status Code
    assert response.status_code == 200, "Endpoint should return HTTP 200"
    
    # 2. Check JSON structure
    data = response.get_json()
    assert data is not None, "Response should be valid JSON"
    assert "positive" in data, "Response JSON must have a 'positive' key"
    
    # 3. Check Data Type (The "Shift Left" Safety Check)
    # We want True/False (bool), not "True"/"False" (str)
    assert isinstance(data['positive'], bool), f"Expected boolean, got {type(data['positive'])}"
