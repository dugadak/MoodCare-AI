# MoodCare API 테스트 가이드

## 🚀 빠른 시작

### 1. Django 서버 실행
```bash
cd moodcare-backend
./run_server.sh
```

서버가 실행되면:
- API: http://127.0.0.1:8000/api/v1/
- Admin: http://127.0.0.1:8000/admin/

### 2. Python API 테스트
```bash
cd moodcare-backend
python test_api.py
```

### 3. Flutter 앱 테스트
```bash
cd moodcare_app
flutter run
```

앱에서 테스트 화면 접근:
- 홈 화면 → 설정 → API 테스트
- 또는 직접 route: `/test`

## 📋 테스트 항목

### Authentication (인증)
- ✅ 회원가입
- ✅ 로그인
- ✅ 프로필 조회
- ✅ 토큰 리프레시
- ✅ 로그아웃

### Emotion (감정 분석)
- ✅ 텍스트 감정 분석
- ✅ 음성 감정 분석
- ✅ 감정 기록 생성
- ✅ 감정 기록 조회
- ✅ 감정 통계/인사이트

### Story (스토리텔링)
- ✅ AI 스토리 생성
- ✅ 스토리 목록 조회
- ✅ 스토리 선택지 처리
- ✅ 스토리 저장/삭제
- ✅ 템플릿 조회

### Music (음악 추천)
- ✅ AI 음악 추천
- ✅ 플레이리스트 조회
- ✅ 음악 프로필 관리
- ✅ 음악 일기 작성
- ✅ 피드백 수집

## 🔧 환경 설정

### .env 파일 설정
```bash
cd moodcare-backend
cp .env.example .env
# .env 파일 편집하여 API 키 추가
```

필수 환경 변수:
- `OPENAI_API_KEY`: GPT-4 사용
- `SPOTIFY_CLIENT_ID`: 음악 추천
- `SPOTIFY_CLIENT_SECRET`: 음악 추천

### 테스트 계정
- Username: `testuser`
- Password: `testpass123`
- Email: `test@moodcare.com`

## 📱 Flutter 테스트 화면

### API 테스트 화면 기능
1. **개별 테스트**: Auth, Emotion, Story, Music 각각 테스트
2. **전체 테스트**: 모든 API 순차 테스트
3. **실시간 결과**: 각 테스트 성공/실패 및 응답 시간 표시
4. **결과 요약**: 전체 성공률 및 실패 항목 표시

### 테스트 화면 추가 방법
```dart
// main.dart의 라우터에 추가
GoRoute(
  path: '/test',
  builder: (context, state) => const APITestScreen(),
),
```

## 🐛 디버깅

### 서버 로그 확인
```bash
tail -f moodcare-backend/server.log
```

### Django 디버그 모드
```python
# settings.py
DEBUG = True  # 개발 중에만
```

### Flutter 디버그 출력
```dart
// API 서비스에서 로그 활성화
ApiService.enableDebugLog = true;
```

## 📊 테스트 결과 예시

```
🚀 Starting MoodCare API Tests
📍 Target: http://127.0.0.1:8000/api/v1
✅ Server is running

📋 Authentication Tests
==================================================
✅ PASS | User Registration
✅ PASS | User Login
✅ PASS | Get Profile
✅ PASS | Token Refresh

📋 Emotion Analysis Tests
==================================================
✅ PASS | Text Emotion Analysis
✅ PASS | Create Emotion Record
✅ PASS | Get Emotion History
✅ PASS | Get Emotion Insights

📊 Test Summary
==================================================
Total Tests: 16
✅ Passed: 16
❌ Failed: 0
Success Rate: 100.0%
```

## 🚨 일반적인 문제 해결

### 1. 서버 연결 실패
- Django 서버가 실행 중인지 확인
- 포트 8000이 사용 중인지 확인
- 방화벽 설정 확인

### 2. 인증 오류
- 토큰이 만료되었는지 확인
- .env 파일의 JWT_SECRET_KEY 확인

### 3. AI 기능 오류
- OpenAI API 키 유효성 확인
- API 사용량 한도 확인

### 4. Flutter 연결 오류
- Android 에뮬레이터: `10.0.2.2:8000` 사용
- iOS 시뮬레이터: `localhost:8000` 사용
- 실제 기기: 같은 네트워크에서 컴퓨터 IP 사용

## 📝 추가 개발 사항

- [ ] WebSocket 실시간 통신 테스트
- [ ] 오프라인 모드 테스트
- [ ] 푸시 알림 테스트
- [ ] 성능 벤치마크 테스트
- [ ] 부하 테스트
- [ ] E2E 자동화 테스트