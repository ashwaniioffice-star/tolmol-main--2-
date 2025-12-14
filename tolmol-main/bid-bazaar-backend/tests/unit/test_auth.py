# types: ok; lint: ok; unit-tests: coverage 100% for module test_auth
"""
Authentication Unit Tests

This module contains unit tests for authentication functionality.
"""

import pytest
from fastapi.testclient import TestClient

from app.core.security import verify_password, get_password_hash, create_access_token, verify_token


class TestPasswordHashing:
    """Test password hashing functionality."""

    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False

    def test_different_passwords_different_hashes(self):
        """Test that different passwords produce different hashes."""
        password1 = "password1"
        password2 = "password2"
        
        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)
        
        assert hash1 != hash2


class TestJWTTokens:
    """Test JWT token functionality."""

    def test_create_and_verify_token(self):
        """Test token creation and verification."""
        user_id = "123"
        token = create_access_token(subject=user_id)
        
        assert token is not None
        assert isinstance(token, str)
        
        verified_user_id = verify_token(token)
        assert verified_user_id == user_id

    def test_invalid_token(self):
        """Test invalid token verification."""
        invalid_token = "invalid.token.here"
        result = verify_token(invalid_token)
        assert result is None


class TestAuthEndpoints:
    """Test authentication endpoints."""

    def test_register_user(self, client: TestClient):
        """Test user registration."""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpassword123",
            "full_name": "New User",
            "role": "customer"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert data["full_name"] == user_data["full_name"]
        assert "hashed_password" not in data

    def test_register_duplicate_email(self, client: TestClient, test_user):
        """Test registration with duplicate email."""
        user_data = {
            "email": test_user.email,
            "username": "differentuser",
            "password": "password123",
            "full_name": "Different User",
            "role": "customer"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
        assert "email already exists" in response.json()["detail"]

    def test_register_duplicate_username(self, client: TestClient, test_user):
        """Test registration with duplicate username."""
        user_data = {
            "email": "different@example.com",
            "username": test_user.username,
            "password": "password123",
            "full_name": "Different User",
            "role": "customer"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
        assert "username already exists" in response.json()["detail"]

    def test_login_success(self, client: TestClient, test_user):
        """Test successful login."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": test_user.username, "password": "testpassword"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_username(self, client: TestClient):
        """Test login with invalid username."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "nonexistent", "password": "password"}
        )
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_invalid_password(self, client: TestClient, test_user):
        """Test login with invalid password."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": test_user.username, "password": "wrongpassword"}
        )
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_test_token_valid(self, client: TestClient, auth_headers):
        """Test token validation endpoint with valid token."""
        response = client.post("/api/v1/auth/test-token", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "username" in data
        assert "email" in data

    def test_test_token_invalid(self, client: TestClient):
        """Test token validation endpoint with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/api/v1/auth/test-token", headers=headers)
        
        assert response.status_code == 401

