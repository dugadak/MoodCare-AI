#!/usr/bin/env python3
"""
MoodCare API Test Script
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def test_api():
    print("🧪 MoodCare API Testing")
    print("=" * 50)
    
    # 1. Test API Root
    print("\n1. Testing API Root...")
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # 2. Test Registration
    print("\n2. Testing User Registration...")
    register_data = {
        "username": f"testuser_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "email": f"test_{datetime.now().strftime('%Y%m%d%H%M%S')}@test.com",
        "password": "TestPassword123!",
        "password2": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User"
    }
    response = requests.post(f"{BASE_URL}/users/register/", json=register_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print("   ✅ Registration successful!")
    else:
        print(f"   ❌ Registration failed: {response.text}")
    
    # 3. Test Login
    print("\n3. Testing User Login...")
    login_data = {
        "username": register_data["username"],
        "password": register_data["password"]
    }
    response = requests.post(f"{BASE_URL}/users/login/", json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Login successful!")
        tokens = response.json()
        access_token = tokens.get("access")
        print(f"   Access Token: {access_token[:20]}...")
        
        # 4. Test Authenticated Endpoints
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Test Profile
        print("\n4. Testing Profile Endpoint...")
        response = requests.get(f"{BASE_URL}/users/profile/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            profile = response.json()
            print(f"   ✅ Profile fetched: {profile.get('username')}")
        
        # Test Emotion Creation
        print("\n5. Testing Emotion Creation...")
        emotion_data = {
            "emotion_type": "joy",
            "intensity": 8,
            "note": "Test emotion - feeling great!",
            "location": "Home",
            "activity": "Testing API",
            "weather": "Sunny"
        }
        response = requests.post(f"{BASE_URL}/emotions/", json=emotion_data, headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ Emotion created successfully!")
            emotion = response.json()
            emotion_id = emotion.get("id")
        
        # Test Emotion List
        print("\n6. Testing Emotion List...")
        response = requests.get(f"{BASE_URL}/emotions/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            emotions = response.json()
            if isinstance(emotions, list):
                count = len(emotions)
            else:
                count = len(emotions.get('results', []))
            print(f"   ✅ Fetched {count} emotions")
        
        # Test Stats
        print("\n7. Testing Emotion Stats...")
        response = requests.get(f"{BASE_URL}/emotions/stats/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"   ✅ Stats: Total records: {stats.get('total_records')}")
    else:
        print(f"   ❌ Login failed: {response.text}")
    
    print("\n" + "=" * 50)
    print("✨ Testing Complete!")

if __name__ == "__main__":
    test_api()