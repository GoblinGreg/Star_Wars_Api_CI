import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    """Test the home route with name argument"""
    response = client.get('/?name=Luke')
    assert response.status_code == 200
    assert b'Luke' in response.data or b'Characters' in response.data


def test_home_route_without_name(client):
    """Test the home route without name argument"""
    response = client.get('/')
    assert response.status_code == 200


def test_css_included(client):
    """Test that CSS is included correctly"""
    response = client.get('/')
    assert response.status_code == 200
    # Sprawdź czy w HTML jest link do CSS
    assert b'style.css' in response.data or b'stylesheet' in response.data


def test_contact_route_get(client):
    """Test contact route with GET method"""
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'email' in response.data
    assert b'message' in response.data


def test_contact_route_post(client):
    """Test contact route with POST method"""
    response = client.post('/contact', data={
        'email': 'test@example.com',
        'message': 'Test message'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks' in response.data or b'Thank' in response.data
