
import pytest
import json
from geometor.explorer.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Initialize the model before yielding the client
    with app.test_client() as client:
        # We need to manually initialize the model because run() is not called in test environment
        from geometor.explorer.app import new_model
        new_model()
        yield client


def get_elements_by_type(data, type_name):
    return [el for el in data['elements'] if el['type'] == type_name]

def get_element_by_id(data, element_id):
    for el in data['elements']:
        if el['ID'] == element_id:
            return el
    return None

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_get_model(client):
    rv = client.get('/api/model')
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert 'elements' in data
    assert isinstance(data['elements'], list)

def test_new_model(client):
    rv = client.post('/api/model/new', json={'template': 'default'})
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert 'elements' in data
    # Default template has 2 points
    points = get_elements_by_type(data, 'point')
    assert len(points) >= 2

def test_construct_point(client):
    # First ensure we have a clean model
    client.post('/api/model/new', json={'template': 'blank'})
    
    rv = client.post('/api/construct/point', json={'x': '0', 'y': '0'})
    assert rv.status_code == 200
    data = json.loads(rv.data)
    points = get_elements_by_type(data, 'point')
    assert len(points) == 1
    
    # Check if the point is actually there and has correct coordinates
    assert points[0]['x'] == 0.0
    assert points[0]['y'] == 0.0

def test_construct_line(client):
    # Setup: Create two points
    client.post('/api/model/new', json={'template': 'blank'})
    r1 = client.post('/api/construct/point', json={'x': '0', 'y': '0'})
    r2 = client.post('/api/construct/point', json={'x': '1', 'y': '1'})
    
    data = json.loads(r2.data)
    points = get_elements_by_type(data, 'point')
    p_ids = [p['ID'] for p in points]
    assert len(p_ids) == 2
    
    # Construct line
    rv = client.post('/api/construct/line', json={'pt1': p_ids[0], 'pt2': p_ids[1]})
    assert rv.status_code == 200
    data = json.loads(rv.data)
    lines = get_elements_by_type(data, 'line')
    assert len(lines) == 1

def test_construct_circle(client):
    # Setup: Create two points
    client.post('/api/model/new', json={'template': 'blank'})
    client.post('/api/construct/point', json={'x': '0', 'y': '0'})
    r2 = client.post('/api/construct/point', json={'x': '1', 'y': '0'})
    
    data = json.loads(r2.data)
    points = get_elements_by_type(data, 'point')
    p_ids = [p['ID'] for p in points]
    
    # Construct circle
    rv = client.post('/api/construct/circle', json={'pt1': p_ids[0], 'pt2': p_ids[1]})
    assert rv.status_code == 200
    data = json.loads(rv.data)
    circles = get_elements_by_type(data, 'circle')
    assert len(circles) == 1
