# MoodCare AI - 감정 케어 AI 플랫폼 🌈

<div align="center">
  <img src="docs/logo.png" alt="MoodCare Logo" width="200"/>
  
  [![Flutter](https://img.shields.io/badge/Flutter-3.0+-02569B?logo=flutter)](https://flutter.dev)
  [![Django](https://img.shields.io/badge/Django-4.2+-092E20?logo=django)](https://www.djangoproject.com)
  [![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python)](https://www.python.org)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
</div>

## 📖 소개

MoodCare AI는 사용자의 감정을 분석하고 맞춤형 콘텐츠를 제공하는 혁신적인 감정 케어 플랫폼입니다. GPT-4 기반 AI가 사용자의 감정을 이해하고, 스토리텔링과 음악 추천을 통해 정서적 지원을 제공합니다.

### ✨ 주요 기능

- 🎭 **AI 감정 분석**: 텍스트/음성 기반 감정 분석 및 패턴 인식
- 📚 **인터랙티브 스토리텔링**: 감정 맞춤형 AI 스토리 생성
- 🎵 **음악 치료**: 감정 기반 음악 추천 및 치료적 사운드
- 💬 **실시간 감정 공유**: WebSocket 기반 실시간 커뮤니케이션
- 📱 **오프라인 모드**: 네트워크 없이도 사용 가능
- 🔔 **스마트 알림**: FCM 기반 맞춤형 푸시 알림

## 🏗️ 프로젝트 구조

```
MoodCare-Project/
├── moodcare-backend/       # Django REST API 서버
│   ├── emotions/          # 감정 분석 모듈
│   ├── stories/           # 스토리텔링 모듈
│   ├── music/             # 음악 추천 모듈
│   ├── notifications/     # 알림 시스템
│   ├── realtime/          # WebSocket 통신
│   └── users/             # 사용자 인증
├── moodcare_app/          # Flutter 모바일 앱
│   ├── lib/
│   │   ├── screens/       # UI 화면
│   │   ├── providers/     # 상태 관리
│   │   ├── services/      # API 서비스
│   │   └── widgets/       # 재사용 컴포넌트
│   └── assets/           # 리소스 파일
└── docs/                 # 문서
```

## 🚀 시작하기

### 필수 요구사항

- Python 3.9+
- Flutter 3.0+
- PostgreSQL 13+
- Redis 6.0+
- Node.js 16+ (Firebase CLI용)

### 백엔드 설정

1. **저장소 클론**
```bash
git clone https://github.com/dugadak/MoodCare-AI.git
cd MoodCare-Project
```

2. **가상환경 설정**
```bash
cd moodcare-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **의존성 설치**
```bash
pip install -r requirements.txt
```

4. **환경변수 설정**
`.env` 파일 생성:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost/moodcare
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your-openai-api-key
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
```

5. **데이터베이스 마이그레이션**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. **서버 실행**
```bash
# 개발 서버
python manage.py runserver

# WebSocket 서버 (Daphne)
daphne -b 0.0.0.0 -p 8000 moodcare.asgi:application
```

### 프론트엔드 설정

1. **Flutter 의존성 설치**
```bash
cd moodcare_app
flutter pub get
```

2. **Firebase 설정**
- Firebase 콘솔에서 프로젝트 생성
- `google-services.json` (Android) 및 `GoogleService-Info.plist` (iOS) 추가
- Firebase CLI로 초기화:
```bash
firebase init
```

3. **앱 실행**
```bash
flutter run
```

## 📚 API 문서

### 인증 API

#### 회원가입
```http
POST /api/v1/auth/register/
Content-Type: application/json

{
  "username": "user123",
  "email": "user@example.com",
  "password": "securepassword",
  "profile": {
    "birth_date": "1990-01-01",
    "gender": "female"
  }
}
```

#### 로그인
```http
POST /api/v1/auth/login/
Content-Type: application/json

{
  "username": "user123",
  "password": "securepassword"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1...",
  "refresh": "eyJ0eXAiOiJKV1...",
  "user": {...}
}
```

### 감정 분석 API

#### 텍스트 감정 분석
```http
POST /api/v1/emotions/records/analyze_text/
Authorization: Bearer {token}
Content-Type: application/json

{
  "text": "오늘은 정말 기분이 좋아요!",
  "situation": "친구들과 만남"
}

Response:
{
  "emotion_type": "happy",
  "sub_emotion": "joyful",
  "intensity": 8.5,
  "triggers": ["social", "friendship"],
  "recommendations": [...]
}
```

#### 감정 통계
```http
GET /api/v1/emotions/records/statistics/?days=30
Authorization: Bearer {token}

Response:
{
  "total_records": 120,
  "emotion_distribution": {
    "happy": 45,
    "sad": 20,
    "anxious": 30,
    "peaceful": 25
  },
  "average_intensity": 6.5,
  "hourly_distribution": {...},
  "top_triggers": [...]
}
```

#### 감정 트렌드
```http
GET /api/v1/emotions/records/trends/?days=7
Authorization: Bearer {token}

Response:
{
  "daily_trends": [...],
  "weekly_pattern": [...],
  "trend_direction": "improving"
}
```

#### AI 인사이트
```http
GET /api/v1/emotions/records/insights/
Authorization: Bearer {token}

Response:
{
  "insights": [...],
  "patterns": [...],
  "recommendations": [...],
  "emotional_balance_score": 75.5
}
```

### 스토리텔링 API

#### AI 스토리 생성
```http
POST /api/v1/stories/stories/generate/
Authorization: Bearer {token}
Content-Type: application/json

{
  "emotion": "anxious",
  "theme": "overcoming",
  "prompt": "새로운 도전에 대한 불안감"
}

Response:
{
  "id": 1,
  "title": "작은 용기의 시작",
  "content": "...",
  "choices": [
    {
      "id": "a",
      "text": "도전을 받아들인다",
      "next_chapter": 2
    },
    {
      "id": "b",
      "text": "조금 더 준비한다",
      "next_chapter": 3
    }
  ]
}
```

### 음악 추천 API

#### 감정 기반 음악 추천
```http
POST /api/v1/music/recommendations/generate/
Authorization: Bearer {token}
Content-Type: application/json

{
  "emotion": "peaceful",
  "intensity": 7,
  "preferences": {
    "genre": ["classical", "ambient"],
    "energy": "low"
  }
}

Response:
{
  "recommendations": [
    {
      "track_name": "Claire de Lune",
      "artist": "Claude Debussy",
      "spotify_id": "...",
      "features": {
        "valence": 0.3,
        "energy": 0.2,
        "tempo": 68
      }
    }
  ]
}
```

### 알림 API

#### FCM 토큰 등록
```http
POST /api/v1/notifications/tokens/register/
Authorization: Bearer {token}
Content-Type: application/json

{
  "token": "fcm_token_here",
  "device_type": "ios",
  "device_id": "unique_device_id"
}
```

#### 알림 설정 조회/수정
```http
GET /api/v1/notifications/preferences/current/
PUT /api/v1/notifications/preferences/current/
Authorization: Bearer {token}

{
  "emotion_reminder": true,
  "story_updates": true,
  "music_recommendations": false,
  "daily_reminder_enabled": true,
  "daily_reminder_time": "20:00",
  "quiet_hours_enabled": false
}
```

### WebSocket 연결

#### 실시간 채팅
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat/room1/');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'message',
    message: 'Hello!',
    username: 'user123'
  }));
};
```

#### 실시간 감정 공유
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/emotion/');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'share_emotion',
    emotion: 'happy',
    intensity: 8,
    message: '오늘 정말 좋은 일이 있었어요!'
  }));
};
```

## 🛠️ 기술 스택

### Backend
- **Framework**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL, Redis
- **AI/ML**: OpenAI GPT-4, NumPy, Pandas
- **Real-time**: Django Channels, WebSocket
- **Push Notifications**: Firebase Admin SDK
- **Authentication**: JWT (djangorestframework-simplejwt)

### Frontend
- **Framework**: Flutter 3.0+
- **State Management**: Provider Pattern
- **Network**: Dio, WebSocket
- **Local Storage**: SQLite (sqflite)
- **Push Notifications**: Firebase Messaging
- **UI/UX**: Custom 3D Animations, Glassmorphism

## 📱 주요 화면

### 1. 홈 대시보드
- 오늘의 감정 요약
- 3D 감정 구체 시각화
- 추천 콘텐츠 카드
- 빠른 감정 체크인

### 2. 감정 입력
- 텍스트/음성 입력 모드
- 실시간 감정 분석
- 감정 태그 선택
- 상황 컨텍스트 입력

### 3. 스토리 화면
- 3D 책장 애니메이션
- 인터랙티브 스토리 선택
- 페이지 넘김 효과
- 스토리 저장/공유

### 4. 음악 플레이어
- 3D 비닐 레코드 애니메이션
- 실시간 비주얼라이저
- 감정 기반 플레이리스트
- 음악 일기 작성

### 5. 알림 센터
- 알림 목록 및 필터링
- 카테고리별 알림 설정
- 리마인더 설정
- 방해금지 모드

## 🧪 테스트

### 백엔드 테스트
```bash
cd moodcare-backend
python manage.py test

# API 통합 테스트
python test_api.py
```

### 프론트엔드 테스트
```bash
cd moodcare_app
flutter test
```

## 📈 성능 최적화

- **캐싱**: Redis를 활용한 API 응답 캐싱
- **이미지 최적화**: WebP 형식 사용, 레이지 로딩
- **코드 스플리팅**: 동적 임포트로 초기 로딩 시간 단축
- **오프라인 우선**: SQLite 로컬 DB로 네트워크 의존도 감소
- **배치 처리**: 동기화 큐를 통한 효율적인 데이터 동기화

## 🔒 보안

- JWT 기반 인증
- HTTPS 통신 암호화
- SQL Injection 방지
- XSS/CSRF 보호
- 민감 정보 암호화 저장
- Rate Limiting 적용

## 📊 데이터베이스 스키마

### EmotionRecord
- `id`: Primary Key
- `user_id`: Foreign Key (User)
- `emotion_type`: 감정 유형
- `sub_emotion`: 세부 감정
- `intensity`: 감정 강도 (1-10)
- `text`: 입력 텍스트
- `ai_analysis`: AI 분석 결과 (JSON)
- `triggers`: 트리거 목록
- `created_at`: 생성 시간

### Story
- `id`: Primary Key
- `user_id`: Foreign Key (User)
- `title`: 스토리 제목
- `content`: 스토리 내용
- `emotion`: 관련 감정
- `theme`: 스토리 테마
- `current_chapter`: 현재 챕터
- `choices_made`: 선택 기록 (JSON)
- `created_at`: 생성 시간

### NotificationLog
- `id`: Primary Key
- `user_id`: Foreign Key (User)
- `title`: 알림 제목
- `body`: 알림 내용
- `category`: 알림 카테고리
- `status`: 발송 상태
- `sent_at`: 발송 시간
- `read_at`: 읽음 시간

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 팀

- **개발**: MoodCare Team
- **디자인**: UI/UX Team
- **기획**: Product Team

## 📞 문의

- Email: support@moodcare.ai
- Website: https://moodcare.ai
- Issues: [GitHub Issues](https://github.com/dugadak/MoodCare-AI/issues)

---

<div align="center">
  Made with ❤️ by MoodCare Team
</div>