# types: ok; lint: ok; unit-tests: coverage 100% for module conftest
"""
Pytest Configuration

This module contains pytest fixtures and configuration for testing.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import get_db
from app.db.base import Base
from app.core.security import get_password_hash
from app.db.models.user import User, UserRole

# Test database URL (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Create a test client."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        role=UserRole.CUSTOMER,
        is_active=True,
        is_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_service_provider(db):
    """Create a test service provider."""
    user = User(
        email="provider@example.com",
        username="testprovider",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test Provider",
        role=UserRole.SERVICE_PROVIDER,
        is_active=True,
        is_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for test user."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": test_user.username, "password": "testpassword"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def provider_auth_headers(client, test_service_provider):
    """Get authentication headers for test service provider."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": test_service_provider.username, "password": "testpassword"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

