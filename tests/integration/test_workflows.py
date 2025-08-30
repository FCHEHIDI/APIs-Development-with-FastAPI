"""
Integration tests for the complete API workflow.
"""
import pytest
from fastapi.testclient import TestClient


class TestAPIWorkflow:
    """Test complete API workflow scenarios."""
    
    def test_complete_user_workflow(self, client: TestClient):
        """Test complete user registration and authentication workflow."""
        # 1. Register a new user
        user_data = {
            "email": "workflow@example.com",
            "username": "workflowuser",
            "full_name": "Workflow User",
            "password": "workflowpass123"
        }
        
        register_response = client.post("/api/v1/auth/register", json=user_data)
        assert register_response.status_code == 201
        user_id = register_response.json()["id"]
        
        # 2. Login with the new user
        login_data = {
            "username": "workflowuser",
            "password": "workflowpass123"
        }
        
        login_response = client.post("/api/v1/auth/login/json", json=login_data)
        assert login_response.status_code == 200
        
        token = login_response.json()["access_token"]
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Get user profile
        profile_response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert profile_response.status_code == 200
        assert profile_response.json()["username"] == "workflowuser"
        
        # 4. Update user profile
        update_data = {"full_name": "Updated Workflow User"}
        update_response = client.put(
            "/api/v1/users/me", 
            json=update_data, 
            headers=auth_headers
        )
        assert update_response.status_code == 200
        assert update_response.json()["full_name"] == "Updated Workflow User"
    
    def test_complete_post_workflow(self, client: TestClient, auth_headers):
        """Test complete post management workflow."""
        # 1. Create a new post
        post_data = {
            "title": "Test Post",
            "content": "This is a test post content.",
            "is_published": False
        }
        
        create_response = client.post(
            "/api/v1/posts/", 
            json=post_data, 
            headers=auth_headers
        )
        assert create_response.status_code == 201
        
        post_id = create_response.json()["id"]
        assert create_response.json()["title"] == post_data["title"]
        assert create_response.json()["is_published"] is False
        
        # 2. Get the created post
        get_response = client.get(f"/api/v1/posts/{post_id}", headers=auth_headers)
        assert get_response.status_code == 200
        assert get_response.json()["title"] == post_data["title"]
        
        # 3. Update the post
        update_data = {
            "title": "Updated Test Post",
            "is_published": True
        }
        
        update_response = client.put(
            f"/api/v1/posts/{post_id}", 
            json=update_data, 
            headers=auth_headers
        )
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Updated Test Post"
        assert update_response.json()["is_published"] is True
        
        # 4. List all posts (should include the published post)
        list_response = client.get("/api/v1/posts/")
        assert list_response.status_code == 200
        posts = list_response.json()
        assert len(posts) >= 1
        
        # 5. List user's own posts
        my_posts_response = client.get("/api/v1/posts/my-posts", headers=auth_headers)
        assert my_posts_response.status_code == 200
        my_posts = my_posts_response.json()
        assert len(my_posts) >= 1
        
        # 6. Delete the post
        delete_response = client.delete(
            f"/api/v1/posts/{post_id}", 
            headers=auth_headers
        )
        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == "Post deleted successfully"
        
        # 7. Verify post is deleted
        get_deleted_response = client.get(f"/api/v1/posts/{post_id}")
        assert get_deleted_response.status_code == 404
    
    def test_permission_workflow(self, client: TestClient, auth_headers, superuser_headers):
        """Test permission and authorization workflow."""
        # 1. Regular user tries to access admin endpoint
        admin_response = client.get("/api/v1/users/", headers=auth_headers)
        assert admin_response.status_code == 403
        
        # 2. Superuser accesses admin endpoint
        admin_response = client.get("/api/v1/users/", headers=superuser_headers)
        assert admin_response.status_code == 200
        
        # 3. Create a post as regular user
        post_data = {
            "title": "Permission Test Post",
            "content": "Testing permissions.",
            "is_published": True
        }
        
        create_response = client.post(
            "/api/v1/posts/", 
            json=post_data, 
            headers=auth_headers
        )
        assert create_response.status_code == 201
        post_id = create_response.json()["id"]
        
        # 4. Try to update someone else's post (should fail without superuser headers)
        # First, create another user's post using superuser
        post_data_admin = {
            "title": "Admin Post",
            "content": "This is an admin post.",
            "is_published": True
        }
        
        admin_post_response = client.post(
            "/api/v1/posts/", 
            json=post_data_admin, 
            headers=superuser_headers
        )
        assert admin_post_response.status_code == 201
        admin_post_id = admin_post_response.json()["id"]
        
        # Regular user tries to update admin's post
        update_data = {"title": "Hacked Post"}
        hack_response = client.put(
            f"/api/v1/posts/{admin_post_id}", 
            json=update_data, 
            headers=auth_headers
        )
        assert hack_response.status_code == 404  # Should not find post owned by other user
    
    def test_validation_workflow(self, client: TestClient):
        """Test input validation workflow."""
        # 1. Test invalid email registration
        invalid_email_data = {
            "email": "invalid-email",
            "username": "validuser",
            "password": "validpassword123"
        }
        
        response = client.post("/api/v1/auth/register", json=invalid_email_data)
        assert response.status_code == 422
        
        # 2. Test short password
        short_password_data = {
            "email": "valid@example.com",
            "username": "validuser",
            "password": "123"
        }
        
        response = client.post("/api/v1/auth/register", json=short_password_data)
        assert response.status_code == 422
        
        # 3. Test missing required fields
        incomplete_data = {
            "email": "test@example.com"
            # Missing username and password
        }
        
        response = client.post("/api/v1/auth/register", json=incomplete_data)
        assert response.status_code == 422
    
    def test_error_handling_workflow(self, client: TestClient):
        """Test error handling scenarios."""
        # 1. Test 404 errors
        response = client.get("/api/v1/posts/99999")
        assert response.status_code == 404
        
        # 2. Test unauthorized access
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
        
        # 3. Test invalid token
        invalid_headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/api/v1/auth/me", headers=invalid_headers)
        assert response.status_code == 401
