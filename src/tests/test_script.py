import pytest
from fastapi.testclient import TestClient
from main import app  # import your FastAPI app

client = TestClient(app)

def test_get_signup_page():
    response = client.get("/signup")
    assert response.status_code == 200
    assert "signup" in response.text.lower()

def test_create_user_success(monkeypatch):
    # Mock DB session
    class DummyDB:
        def query(self, model):
            return self
        def filter(self, condition):
            return self
        def first(self):
            return None
        def add(self, obj): pass
        def commit(self): pass
        def refresh(self, obj): pass

    def fake_get_db():
        yield DummyDB()

    app.dependency_overrides[fake_get_db] = fake_get_db

    response = client.post("/signup", data={"email": "test@example.com", "password": "secret"})
    assert response.status_code == 200
    assert "test@example.com" in response.text
