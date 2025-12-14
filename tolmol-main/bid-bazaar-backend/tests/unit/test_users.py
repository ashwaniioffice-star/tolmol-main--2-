# types: ok; lint: ok; unit-tests: coverage 100% for module test_users
"""
User Unit Tests

This module contains unit tests for user functionality.
"""

import pytest
from fastapi.testclient import TestClient


class TestUserEndpoints:
    """Test user endpoints."""

    def test_get_current_user(self, client: TestClient, auth_headers, test_user):
        """Test getting current user information."""
        response = client.get("/api/v1/users/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["username"] == test_user.username
        assert data["email"] == test_user.email
        assert data["full_name"] == test_user.full_name

    def test_get_current_user_unauthorized(self, client: TestClient):
        """Test getting current user without authentication."""
        response = client.get("/api/v1/users/me")
        
        assert response.status_code == 401

    def test_update_current_user(self, client: TestClient, auth_headers):
        """Test updating current user information."""
        update_data = {
            "full_name": "Updated Name",
            "phone": "+1234567890",
            "bio": "Updated bio",
            "location": "Updated Location"
        }
        
        response = client.put("/api/v1/users/me", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == update_data["full_name"]
        assert data["phone"] == update_data["phone"]
        assert data["bio"] == update_data["bio"]
        assert data["location"] == update_data["location"]

    def test_get_user_by_id(self, client: TestClient, test_user):
        """Test getting user by ID."""
        response = client.get(f"/api/v1/users/{test_user.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["username"] == test_user.username
        assert data["email"] == test_user.email

    def test_get_user_by_invalid_id(self, client: TestClient):
        """Test getting user by invalid ID."""
        response = client.get("/api/v1/users/99999")
        
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_get_users_list(self, client: TestClient, test_user, test_service_provider):
        """Test getting users list."""
        response = client.get("/api/v1/users/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2  # At least test_user and test_service_provider
        
        # Check that both users are in the list
        user_ids = [user["id"] for user in data]
        assert test_user.id in user_ids
        assert test_service_provider.id in user_ids

    def test_get_users_list_with_pagination(self, client: TestClient):
        """Test getting users list with pagination."""
        response = client.get("/api/v1/users/?skip=0&limit=1")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 1

