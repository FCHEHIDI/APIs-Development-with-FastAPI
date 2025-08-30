"""
API Test Script - Demonstrates FastAPI functionality

This script tests the main API endpoints to show the application working.
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"
API_V1 = f"{BASE_URL}/api/v1"

def test_api():
    """Test the main API functionality."""
    
    print("🚀 FastAPI Professional API Test")
    print("=" * 50)
    
    # 1. Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print("❌ Health check failed")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the server first:")
        print("   python run.py")
        return
    
    # 2. Test Root Endpoint
    print("\n2. Testing Root Endpoint...")
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        print("✅ Root endpoint working")
        print(f"   Response: {response.json()}")
    
    # 3. Register a new user
    print("\n3. Testing User Registration...")
    user_data = {
        "email": "demo@example.com",
        "username": "demouser",
        "full_name": "Demo User",
        "password": "demopassword123"
    }
    
    response = requests.post(f"{API_V1}/auth/register", json=user_data)
    if response.status_code == 201:
        print("✅ User registration successful")
        user_info = response.json()
        print(f"   User ID: {user_info['id']}")
        print(f"   Username: {user_info['username']}")
    else:
        print("❌ User registration failed")
        print(f"   Error: {response.json()}")
        if response.status_code == 400 and "already" in response.json().get("detail", ""):
            print("   (User might already exist - continuing with login)")
    
    # 4. Login and get token
    print("\n4. Testing User Login...")
    login_data = {
        "username": "demouser",
        "password": "demopassword123"
    }
    
    response = requests.post(f"{API_V1}/auth/login/json", json=login_data)
    if response.status_code == 200:
        print("✅ User login successful")
        token_data = response.json()
        access_token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        print(f"   Token type: {token_data['token_type']}")
    else:
        print("❌ User login failed")
        print(f"   Error: {response.json()}")
        return
    
    # 5. Get current user info
    print("\n5. Testing Get Current User...")
    response = requests.get(f"{API_V1}/auth/me", headers=headers)
    if response.status_code == 200:
        print("✅ Get current user successful")
        user_info = response.json()
        print(f"   Username: {user_info['username']}")
        print(f"   Email: {user_info['email']}")
    
    # 6. Create a post
    print("\n6. Testing Post Creation...")
    post_data = {
        "title": "My First API Post",
        "content": "This post was created through the FastAPI backend!",
        "is_published": True
    }
    
    response = requests.post(f"{API_V1}/posts/", json=post_data, headers=headers)
    if response.status_code == 201:
        print("✅ Post creation successful")
        post_info = response.json()
        post_id = post_info["id"]
        print(f"   Post ID: {post_id}")
        print(f"   Title: {post_info['title']}")
    
    # 7. Get all posts
    print("\n7. Testing Get All Posts...")
    response = requests.get(f"{API_V1}/posts/")
    if response.status_code == 200:
        posts = response.json()
        print(f"✅ Retrieved {len(posts)} posts")
        if posts:
            print(f"   Latest post: {posts[0]['title']}")
    
    # 8. Update the post
    print("\n8. Testing Post Update...")
    update_data = {
        "title": "Updated API Post",
        "content": "This post has been updated through the API!"
    }
    
    response = requests.put(f"{API_V1}/posts/{post_id}", json=update_data, headers=headers)
    if response.status_code == 200:
        print("✅ Post update successful")
        updated_post = response.json()
        print(f"   New title: {updated_post['title']}")
    
    print("\n" + "=" * 50)
    print("🎉 FastAPI Professional API Test Complete!")
    print(f"📖 View full API documentation at: {BASE_URL}/docs")
    print(f"📚 Alternative documentation at: {BASE_URL}/redoc")
    print("=" * 50)


if __name__ == "__main__":
    test_api()
