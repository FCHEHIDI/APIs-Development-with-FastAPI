"""
Unit tests for authentication functionality.
"""
import pytest
from fastapi.testclient import TestClient
from app.core.security import security


class TestAuth:
    """Test authentication endpoints."""
    
    def test_register_user(self, client: TestClient):
        """Test user registration."""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "full_name": "New User",
            "password": "newpassword123"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert data["full_name"] == user_data["full_name"]
        assert "id" in data
        assert data["is_active"] is True
    
    def test_register_duplicate_email(self, client: TestClient, test_user):
        """Test registration with duplicate email."""
        user_data = {
            "email": test_user.email,
            "username": "differentuser",
            "password": "password123"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_register_duplicate_username(self, client: TestClient, test_user):
        """Test registration with duplicate username."""
        user_data = {
            "email": "different@example.com",
            "username": test_user.username,
            "password": "password123"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]
    
    def test_login_success(self, client: TestClient, test_user):
        """Test successful login."""
        login_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        
        response = client.post(
            "/api/v1/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_json_success(self, client: TestClient, test_user):
        """Test successful login with JSON."""
        login_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        
        response = client.post("/api/v1/auth/login/json", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client: TestClient):
        """Test login with invalid credentials."""
        login_data = {
            "username": "wronguser",
            "password": "wrongpassword"
        }
        
        response = client.post("/api/v1/auth/login/json", json=login_data)
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_get_current_user(self, client: TestClient, auth_headers):
        """Test getting current user information."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
    
    def test_get_current_user_unauthorized(self, client: TestClient):
        """Test getting current user without authentication."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    def test_logout(self, client: TestClient, auth_headers):
        """Test user logout."""
        response = client.post("/api/v1/auth/logout", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "logged out" in data["message"]


class TestSecurity:
    """Test security utilities."""
    
    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "testpassword123"
        hashed = security.get_password_hash(password)
        
        assert security.verify_password(password, hashed)
        assert not security.verify_password("wrongpassword", hashed)
    
    def test_token_creation_and_verification(self):
        """Test JWT token creation and verification."""
        data = {"sub": "testuser"}
        token = security.create_access_token(data)
        
        payload = security.verify_token(token)
        assert payload is not None
        assert payload["sub"] == "testuser"
    
    def test_invalid_token_verification(self):
        """Test verification of invalid token."""
        invalid_token = "invalid.jwt.token"
        payload = security.verify_token(invalid_token)
        assert payload is None
