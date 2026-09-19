import pytest
import httpx
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import src.database
from src.database import Base, User, get_db
from main import app

# Setup in-memory SQLite DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[src.database.get_db] = override_get_db
client = TestClient(app)

def test_create_user_integration():
    response = client.post("/signup", data={"email": "integration@example.com", "password": "secret"})
    assert response.status_code == 200

    # Verify user in DB
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "integration@example.com").first()
    assert user is not None
    assert user.email == "integration@example.com"
