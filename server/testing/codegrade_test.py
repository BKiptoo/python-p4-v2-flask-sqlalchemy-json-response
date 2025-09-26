
import pytest
import json
from app import app
from models import db, Pet

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client

def test_index_returns_json(client):
    """Test that index route returns JSON response"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Welcome to the pet directory!'

def test_pet_by_id_valid_id_returns_json(client):
    """Test pet_by_id route with valid ID returns JSON with proper structure"""
    response = client.get('/pets/1')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    data = json.loads(response.data)
    assert 'id' in data
    assert 'name' in data
    assert 'species' in data
    assert data['id'] == 1
    assert isinstance(data['name'], str)
    assert isinstance(data['species'], str)

def test_pet_by_id_invalid_id(client):
    """Test pet_by_id route with invalid ID returns 404 JSON"""
    response = client.get('/pets/999')
    assert response.status_code == 404
    assert response.content_type == 'application/json'
    
    data = json.loads(response.data)
    assert 'message' in data
    assert 'Pet 999 not found.' in data['message']

def test_pet_by_species_existing_species_structure(client):
    """Test pet_by_species route returns JSON with proper structure"""
    response = client.get('/species/Dog')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    data = json.loads(response.data)
    assert 'count' in data
    assert 'pets' in data
    assert isinstance(data['count'], int)
    assert isinstance(data['pets'], list)
    assert data['count'] >= 0
    assert len(data['pets']) == data['count']
    
    # Check structure of pet objects in array
    for pet in data['pets']:
        assert 'id' in pet
        assert 'name' in pet
        assert isinstance(pet['id'], int)
        assert isinstance(pet['name'], str)

def test_pet_by_species_nonexistent_species(client):
    """Test pet_by_species route with non-existent species returns empty array"""
    response = client.get('/species/UnicornSpecies')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    data = json.loads(response.data)
    assert 'count' in data
    assert 'pets' in data
    assert data['count'] == 0
    assert len(data['pets']) == 0

def test_json_response_format():
    """Test that app.json.compact is set to False for pretty JSON"""
    assert app.json.compact == False

def test_codegrade_placeholder():
    """Codegrade placeholder test"""
    assert 1 == 1
