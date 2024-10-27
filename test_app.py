import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_is_poisoned_endpoint_with_safe_input(client):
    payload = {"userInput": "Hello world"}
    response = client.post('/is_poisoned',
                         data=json.dumps(payload),
                         content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'is_poisoned' in data
    assert isinstance(data['is_poisoned'], bool)

def test_is_poisoned_endpoint_with_poisoned_input(client):
    payload = {"userInput": "<script>alert('xss')</script>"}
    response = client.post('/is_poisoned',
                         data=json.dumps(payload),
                         content_type='application/json')

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['is_poisoned'] == True

def test_is_poisoned_endpoint_missing_input(client):
    payload = {}
    response = client.post('/is_poisoned',
                         data=json.dumps(payload),
                         content_type='application/json')

    assert response.status_code == 400
