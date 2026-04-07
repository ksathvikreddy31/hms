import pytest
from app import create_app
from extensions import db
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "test_secret"

@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    """A simple test to verify the app context is working."""
    response = client.get('/api/auth/login') # Should 405 if exists or 404
    assert response.status_code != 500
