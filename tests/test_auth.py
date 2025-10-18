import pytest
from fastapi import status
from app.auth.jwt_handler import create_access_token, verify_token
from app.auth.utils import hash_password, verify_password

class TestPasswordHashing:
    """Test password hashing and verification."""
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "testpassword"
        hashed = hash_password(password)
        assert hashed != password
        assert len(hashed) > 0
    
    def test_verify_password(self):
        """Test password verification."""
        password = "testpassword"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False

class TestJWTToken:
    """Test JWT token creation and verification."""
    
    def test_create_access_token(self):
        """Test access token creation."""
        data = {"sub": "123"}
        token = create_access_token(data)
        assert token is not None
        assert isinstance(token, str)
    
    def test_verify_token(self):
        """Test token verification."""
        data = {"sub": "123"}
        token = create_access_token(data)
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "123"
    
    def test_verify_invalid_token(self):
        """Test verification of invalid token."""
        payload = verify_token("invalid_token")
        assert payload is None

class TestUserRegistration:
    """Test user registration endpoint."""
    
    def test_register_user_success(self, client):
        """Test successful user registration."""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword"
        }
        response = client.post("/users/register", json=user_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert data["is_admin"] is False
    
    def test_register_user_duplicate_email(self, client, test_user):
        """Test registration with duplicate email."""
        user_data = {
            "username": "anotheruser",
            "email": test_user.email,  # Same email as existing user
            "password": "password"
        }
        response = client.post("/users/register", json=user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]
    
    def test_register_user_invalid_email(self, client):
        """Test registration with invalid email format."""
        user_data = {
            "username": "user",
            "email": "invalid-email",
            "password": "password"
        }
        response = client.post("/users/register", json=user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

class TestUserLogin:
    """Test user login endpoint."""
    
    def test_login_success(self, client, test_user):
        """Test successful login."""
        login_data = {
            "email": test_user.email,
            "password": "testpassword"
        }
        response = client.post("/users/login", json=login_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_email(self, client):
        """Test login with non-existent email."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "password"
        }
        response = client.post("/users/login", json=login_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid email or password" in response.json()["detail"]
    
    def test_login_invalid_password(self, client, test_user):
        """Test login with wrong password."""
        login_data = {
            "email": test_user.email,
            "password": "wrongpassword"
        }
        response = client.post("/users/login", json=login_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid email or password" in response.json()["detail"]

class TestUserProfile:
    """Test user profile endpoint."""
    
    def test_get_me_success(self, client, auth_headers):
        """Test getting current user profile."""
        response = client.get("/users/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "id" in data
        assert "username" in data
        assert "email" in data
        assert "is_admin" in data
    
    def test_get_me_unauthorized(self, client):
        """Test getting profile without authentication."""
        response = client.get("/users/me")
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_me_invalid_token(self, client):
        """Test getting profile with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/users/me", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
