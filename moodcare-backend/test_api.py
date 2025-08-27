#!/usr/bin/env python3
"""
MoodCare API 통합 테스트
모든 엔드포인트를 테스트하고 결과를 출력합니다.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

# API 설정
BASE_URL = "http://127.0.0.1:8000/api/v1"
TEST_USER = {
    "username": "testuser",
    "email": "test@moodcare.com",
    "password": "testpass123",
    "password2": "testpass123",
    "first_name": "Test",
    "last_name": "User"
}

class APITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.access_token = None
        self.refresh_token = None
        self.user_id = None
        self.results = []
        
    def print_result(self, test_name: str, success: bool, message: str = ""):
        """테스트 결과 출력"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}")
        if message:
            print(f"     └─ {message}")
        self.results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
    
    def make_request(self, method: str, endpoint: str, 
                     data: Optional[Dict] = None, 
                     use_auth: bool = False) -> requests.Response:
        """API 요청 헬퍼"""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if use_auth and self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        try:
            if method == "GET":
                return requests.get(url, headers=headers)
            elif method == "POST":
                return requests.post(url, json=data, headers=headers)
            elif method == "PUT":
                return requests.put(url, json=data, headers=headers)
            elif method == "PATCH":
                return requests.patch(url, json=data, headers=headers)
            elif method == "DELETE":
                return requests.delete(url, headers=headers)
        except Exception as e:
            return None
    
    def test_auth_endpoints(self):
        """인증 관련 엔드포인트 테스트"""
        print("\n📋 Authentication Tests")
        print("=" * 50)
        
        # 1. 회원가입
        response = self.make_request("POST", "/auth/register/", TEST_USER)
        if response and response.status_code in [200, 201]:
            self.print_result("User Registration", True, "User created successfully")
            data = response.json()
            self.access_token = data.get("access")
            self.refresh_token = data.get("refresh")
            self.user_id = data.get("user", {}).get("id")
        elif response and response.status_code == 400:
            # 이미 존재하는 유저일 수 있음
            self.print_result("User Registration", True, "User already exists")
        else:
            self.print_result("User Registration", False, 
                            f"Status: {response.status_code if response else 'Connection failed'}")
        
        # 2. 로그인
        login_data = {
            "username": TEST_USER["username"],
            "password": TEST_USER["password"]
        }
        response = self.make_request("POST", "/auth/login/", login_data)
        if response and response.status_code == 200:
            data = response.json()
            self.access_token = data.get("access")
            self.refresh_token = data.get("refresh")
            self.print_result("User Login", True, "Login successful")
        else:
            self.print_result("User Login", False, 
                            f"Status: {response.status_code if response else 'Connection failed'}")
        
        # 3. 프로필 조회
        response = self.make_request("GET", "/auth/profile/", use_auth=True)
        if response and response.status_code == 200:
            self.print_result("Get Profile", True, "Profile retrieved")
        else:
            self.print_result("Get Profile", False, 
                            f"Status: {response.status_code if response else 'Connection failed'}")
        
        # 4. 토큰 리프레시
        if self.refresh_token:
            response = self.make_request("POST", "/auth/token/refresh/", 
                                        {"refresh": self.refresh_token})
            if response and response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access")
                self.print_result("Token Refresh", True, "Token refreshed")
            else:
                self.print_result("Token Refresh", False, 
                                f"Status: {response.status_code if response else 'Connection failed'}")
    
    def test_emotion_endpoints(self):
        """감정 분석 엔드포인트 테스트"""
        print("\n📋 Emotion Analysis Tests")
        print("=" * 50)
        
        # 1. 텍스트 감정 분석
        text_data = {
            "text": "오늘은 정말 행복한 날이에요! 모든 것이 완벽합니다.",
            "context_tags": ["work", "success"]
        }
        response = self.make_request("POST", "/emotions/records/analyze_text/", 
                                    text_data, use_auth=True)
        if response and response.status_code in [200, 201]:
            self.print_result("Text Emotion Analysis", True, "Analysis completed")
        else:
            self.print_result("Text Emotion Analysis", False, 
                            f"Status: {response.status_code if response else 'Connection failed'}")
        
        # 2. 감정 기록 생성
        emotion_data = {
            "emotion_type": "joy",
            "intensity": 8,
            "note": "프로젝트 완료",
            "triggers": ["achievement", "completion"]
        }
        response = self.make_request("POST", "/emotions/records/", 
                                    emotion_data, use_auth=True)
        if response and response.status_code in [200, 201]:
            self.print_result("Create Emotion Record", True, "Record created")
        else:
            self.print_result("Create Emotion Record", False, 
                            f"Status: {response.status_code if response else 'Connection failed'}")
        
        # 3. 감정 기록 조회
        response = self.make_request("GET", "/emotions/records/", use_auth=True)
        if response and response.status_code == 200:
            self.print_result("Get Emotion History", True, 
                            f"Retrieved {len(response.json().get('results', []))} records")
        else:
            self.print_result("Get Emotion History", False, 
                            f"Status: {response.status_code if response else 'Connection failed'}")
        
        # 4. 감정 통계 조회
        response = self.make_request("GET", "/emotions/records/insights/", use_auth=True)
        if response and response.status_code == 200:
            self.print_result("Get Emotion Insights", True, "Insights retrieved")
        else:
            self.print_result("Get Emotion Insights", False, 
                            f"Status: {response.status_code if response else 'Connection failed'}")
    
    def test_story_endpoints(self):
        """스토리텔링 엔드포인트 테스트"""
        print("\n📋 Storytelling Tests")
        print("=" * 50)
        
        # 1. 스토리 생성
        story_data = {
            "emotion": "joy",
            "theme": "adventure",
            "prompt": "용감한 모험가의 이야기"
        }
        response = self.make_request("POST", "/stories/stories/generate/", 
                                    story_data, use_auth=True)
        story_id = None
        if response and response.status_code in [200, 201]:
            self.print_result("Generate Story", True, "Story generated")
            story_id = response.json().get("id")
        else:
            self.print_result("Generate Story", False, 
                            f"Status: {response.status_code if response else 'Connection failed'}")
        
        # 2. 스토리 목록 조회
        response = self.make_request("GET", "/stories/stories/", use_auth=True)
        if response and response.status_code == 200:
            self.print_result("Get Story List", True, 
                            f"Retrieved {len(response.json().get('results', []))} stories")
        else:
            self.print_result("Get Story List", False, 
                            f"Status: {response.status_code if response else 'Connection failed'}")
        
        # 3. 스토리 템플릿 조회
        response = self.make_request("GET", "/stories/templates/", use_auth=True)
        if response and response.status_code == 200:
            self.print_result("Get Story Templates", True, "Templates retrieved")
        else:
            self.print_result("Get Story Templates", False, 
                            f"Status: {response.status_code if response else 'Connection failed'}")
    
    def test_music_endpoints(self):
        """음악 추천 엔드포인트 테스트"""
        print("\n📋 Music Recommendation Tests")
        print("=" * 50)
        
        # 1. 음악 추천 생성
        music_data = {
            "emotion": "calm",
            "preferences": {
                "genre": ["ambient", "classical"],
                "energy_level": "low"
            }
        }
        response = self.make_request("POST", "/music/recommendations/generate/", 
                                    music_data, use_auth=True)
        if response and response.status_code in [200, 201]:
            self.print_result("Generate Music Recommendations", True, 
                            "Recommendations generated")
        else:
            self.print_result("Generate Music Recommendations", False, 
                            f"Status: {response.status_code if response else 'Connection failed'}")
        
        # 2. 음악 프로필 조회
        response = self.make_request("GET", "/music/profile/", use_auth=True)
        if response and response.status_code == 200:
            self.print_result("Get Music Profile", True, "Profile retrieved")
        else:
            self.print_result("Get Music Profile", False, 
                            f"Status: {response.status_code if response else 'Connection failed'}")
        
        # 3. 음악 일기 생성
        diary_data = {
            "emotion": "peaceful",
            "tracks_listened": ["track1", "track2"],
            "note": "편안한 저녁 시간"
        }
        response = self.make_request("POST", "/music/diary/", 
                                    diary_data, use_auth=True)
        if response and response.status_code in [200, 201]:
            self.print_result("Create Music Diary", True, "Diary created")
        else:
            self.print_result("Create Music Diary", False, 
                            f"Status: {response.status_code if response else 'Connection failed'}")
    
    def print_summary(self):
        """테스트 결과 요약"""
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r["success"])
        failed = total - passed
        
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        if failed > 0:
            print("\n⚠️  Failed Tests:")
            for result in self.results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
    
    def run_all_tests(self):
        """모든 테스트 실행"""
        print("\n🚀 Starting MoodCare API Tests")
        print(f"📍 Target: {BASE_URL}")
        print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 서버 연결 확인
        try:
            response = requests.get(f"{self.base_url}/")
            print(f"✅ Server is running")
        except:
            print(f"❌ Cannot connect to server at {self.base_url}")
            print("Please ensure the Django server is running:")
            print("  cd moodcare-backend")
            print("  ./run_server.sh")
            return
        
        # 테스트 실행
        self.test_auth_endpoints()
        self.test_emotion_endpoints()
        self.test_story_endpoints()
        self.test_music_endpoints()
        
        # 결과 요약
        self.print_summary()

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()