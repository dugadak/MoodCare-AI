# 🌟 MoodCare AI - 종합 AI 감정케어 플랫폼

## 📋 프로젝트 개요

MoodCare AI는 최신 AI 기술을 활용한 종합 감정 웰니스 플랫폼입니다. 텍스트와 음성 기반 감정 분석, 인터랙티브 스토리텔링, 맞춤형 음악 추천을 통해 사용자의 정신 건강을 케어합니다.

### 🎯 핵심 기능

#### 1. 🤖 AI 감정 분석
- **텍스트/음성 입력**: 일기, 대화, 음성 메모를 통한 감정 인식
- **실시간 감정 분석**: GPT-4 기반 자연어 처리
- **시각적 피드백**: 감정 상태를 색상과 애니메이션으로 표현
- **감정 트렌드**: 시간별, 일별, 월별 감정 패턴 분석

#### 2. 📚 인터랙티브 스토리텔링
- **AI 스토리 생성**: 사용자 감정에 맞춘 맞춤형 이야기
- **대화형 게임북**: 선택지 기반 스토리 진행
- **치유 스토리**: 감정 상태 개선을 위한 치료적 내러티브
- **창작 모드**: 사용자와 AI가 함께 만드는 협업 스토리

#### 3. 🎵 음악 추천 & 오디오 테라피
- **감정 기반 플레이리스트**: 현재 기분에 맞는 음악 자동 큐레이션
- **오디오 웨이브 시각화**: 음성의 감정을 실시간 시각화
- **ASMR & 백색소음**: 릴랙스를 위한 오디오 콘텐츠
- **음악 일기**: 하루를 음악으로 기록

#### 4. 🎨 감성적 UI/UX
- **다이나믹 테마**: 감정에 따라 변화하는 앱 테마
- **인터랙티브 애니메이션**: 부드러운 전환 효과
- **3D 감정 구체**: 감정 상태를 3D로 시각화
- **햅틱 피드백**: 터치 인터랙션 강화

## 🛠 기술 스택

### Backend (Django 5.2+)
```python
# 핵심 프레임워크
Django==5.2.5
djangorestframework==3.14.0
django-cors-headers==4.3.1

# 인증 & 보안
djangorestframework-simplejwt==5.3.1
python-decouple==3.8
django-ratelimit==4.1.0

# AI & ML
openai==1.35.0
transformers==4.35.0
torch==2.1.0
whisper==1.1.10  # 음성 인식

# 데이터베이스 & 캐시
psycopg2-binary==2.9.9
redis==5.0.1
django-redis==5.4.0

# 실시간 통신
channels==4.0.0
channels-redis==4.2.0
websocket-client==1.7.0

# 음악 & 오디오
spotipy==2.23.0  # Spotify API
pydub==0.25.1
librosa==0.10.1  # 오디오 분석

# 비동기 처리
celery==5.3.4
celery-beat==2.5.0
```

### Frontend (Flutter 3.24+)
```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # 상태 관리 & 라우팅
  provider: ^6.1.1
  go_router: ^13.2.0
  
  # UI 컴포넌트
  flutter_animate: ^4.5.0
  lottie: ^3.1.0
  glassmorphism_ui: ^0.3.0
  
  # API 통신
  dio: ^5.4.0
  web_socket_channel: ^2.4.0
  
  # 오디오 & 음성
  record: ^5.0.4
  just_audio: ^0.9.36
  audio_visualizer: ^0.1.2
  
  # 3D & 애니메이션
  flutter_3d_controller: ^1.2.0
  rive: ^0.12.4
  
  # 기타 유틸리티
  shared_preferences: ^2.2.2
  path_provider: ^2.1.1
  permission_handler: ^11.3.0
```

### Infrastructure
- **Server**: AWS EC2 (t3.medium)
- **Database**: PostgreSQL 15 + Redis
- **Storage**: AWS S3 (미디어 파일)
- **CDN**: CloudFront
- **Container**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana

## 📱 주요 화면 구성

### 1. 홈 대시보드
- 오늘의 감정 요약
- 감정 캘린더
- 추천 콘텐츠 카드
- 빠른 감정 체크인

### 2. 감정 기록
- 텍스트/음성 입력 선택
- 실시간 감정 분석 피드백
- 감정 태그 선택
- 컨텍스트 정보 입력

### 3. 스토리 라운지
- AI 생성 스토리 목록
- 인터랙티브 스토리 플레이어
- 내 스토리 아카이브
- 커뮤니티 공유

### 4. 뮤직 테라피
- 감정 플레이리스트
- 오디오 비주얼라이저
- 음악 일기 타임라인
- 릴랙스 사운드

### 5. 통계 & 인사이트
- 감정 트렌드 차트
- AI 인사이트 리포트
- 패턴 분석
- 성장 기록

## 🔗 API 엔드포인트

### 인증 API
```
POST   /api/v1/auth/register        # 회원가입
POST   /api/v1/auth/login           # 로그인
POST   /api/v1/auth/logout          # 로그아웃
POST   /api/v1/auth/refresh         # 토큰 갱신
GET    /api/v1/auth/profile         # 프로필 조회
PUT    /api/v1/auth/profile         # 프로필 수정
DELETE /api/v1/auth/account         # 회원 탈퇴
```

### 감정 분석 API
```
POST   /api/v1/emotions/analyze/text      # 텍스트 감정 분석
POST   /api/v1/emotions/analyze/voice     # 음성 감정 분석
GET    /api/v1/emotions/records           # 감정 기록 조회
POST   /api/v1/emotions/records           # 감정 기록 생성
GET    /api/v1/emotions/records/{id}      # 감정 상세 조회
PUT    /api/v1/emotions/records/{id}      # 감정 기록 수정
DELETE /api/v1/emotions/records/{id}      # 감정 기록 삭제
GET    /api/v1/emotions/statistics        # 감정 통계
GET    /api/v1/emotions/trends            # 감정 트렌드
GET    /api/v1/emotions/insights          # AI 인사이트
```

### 스토리텔링 API
```
POST   /api/v1/stories/generate           # AI 스토리 생성
GET    /api/v1/stories                    # 스토리 목록
GET    /api/v1/stories/{id}               # 스토리 상세
POST   /api/v1/stories/{id}/interact      # 스토리 상호작용
POST   /api/v1/stories/{id}/save          # 스토리 저장
GET    /api/v1/stories/library            # 내 스토리 라이브러리
POST   /api/v1/stories/{id}/share         # 스토리 공유
```

### 음악 추천 API
```
GET    /api/v1/music/recommendations      # 음악 추천
POST   /api/v1/music/playlists            # 플레이리스트 생성
GET    /api/v1/music/playlists            # 플레이리스트 목록
GET    /api/v1/music/playlists/{id}       # 플레이리스트 상세
PUT    /api/v1/music/playlists/{id}       # 플레이리스트 수정
DELETE /api/v1/music/playlists/{id}       # 플레이리스트 삭제
GET    /api/v1/music/therapy              # 테라피 음악
POST   /api/v1/music/diary                # 음악 일기 작성
```

### 실시간 통신 (WebSocket)
```
ws://api/v1/ws/emotions/realtime          # 실시간 감정 분석
ws://api/v1/ws/stories/interactive        # 인터랙티브 스토리
ws://api/v1/ws/music/visualizer           # 음악 시각화
```

## 🚀 설치 및 실행

### 필수 요구사항
- Python 3.11+
- Flutter 3.24+
- PostgreSQL 15+
- Redis 7+
- Node.js 18+ (선택사항)

### Backend 설정

```bash
# 1. 프로젝트 클론
git clone https://github.com/dugadak/MoodCare-AI.git
cd MoodCare-AI/backend

# 2. 가상환경 생성
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경변수 설정
cp .env.example .env
# .env 파일 편집

# 5. 데이터베이스 마이그레이션
python manage.py makemigrations
python manage.py migrate

# 6. 슈퍼유저 생성
python manage.py createsuperuser

# 7. Static 파일 수집
python manage.py collectstatic

# 8. Redis 실행
redis-server

# 9. Celery 워커 실행 (새 터미널)
celery -A moodcare worker -l info

# 10. 개발 서버 실행
python manage.py runserver
```

### Frontend 설정

```bash
# 1. Flutter 프로젝트로 이동
cd ../frontend

# 2. 의존성 설치
flutter pub get

# 3. API 엔드포인트 설정
# lib/config/api_config.dart 파일 수정

# 4. 앱 실행
flutter run

# iOS 실행
flutter run -d ios

# Android 실행
flutter run -d android
```

### Docker 실행

```bash
# 전체 스택 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down
```

## 📊 데이터베이스 스키마

### Users 테이블
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    birth_date DATE,
    gender VARCHAR(10),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Emotions 테이블
```sql
CREATE TABLE emotions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    emotion_type VARCHAR(50),
    intensity INTEGER,
    source VARCHAR(20), -- text, voice
    raw_text TEXT,
    analysis_result JSONB,
    context JSONB,
    created_at TIMESTAMP
);
```

### Stories 테이블
```sql
CREATE TABLE stories (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    title VARCHAR(255),
    content TEXT,
    story_type VARCHAR(50),
    emotion_tags JSONB,
    interactions JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Music 테이블
```sql
CREATE TABLE music_recommendations (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    emotion_id UUID REFERENCES emotions(id),
    track_id VARCHAR(255),
    track_name VARCHAR(255),
    artist VARCHAR(255),
    recommendation_score FLOAT,
    played_at TIMESTAMP
);
```

## 🧪 테스트

### Backend 테스트
```bash
# 단위 테스트
python manage.py test

# 커버리지 테스트
coverage run --source='.' manage.py test
coverage report

# API 테스트
python manage.py test api.tests
```

### Frontend 테스트
```bash
# 단위 테스트
flutter test

# 위젯 테스트
flutter test test/widget_test.dart

# 통합 테스트
flutter test integration_test
```

## 📝 환경 변수

### Backend (.env)
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database
DATABASE_URL=postgresql://user:password@localhost/moodcare
REDIS_URL=redis://localhost:6379/0

# OpenAI
OPENAI_API_KEY=sk-your-api-key
OPENAI_MODEL=gpt-4-turbo-preview

# Spotify
SPOTIFY_CLIENT_ID=your-client-id
SPOTIFY_CLIENT_SECRET=your-client-secret

# AWS
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET_NAME=moodcare-media

# Security
JWT_ACCESS_TOKEN_LIFETIME=30
JWT_REFRESH_TOKEN_LIFETIME=7
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-app.com

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🚢 배포

### AWS EC2 배포

```bash
# EC2 인스턴스 접속
ssh -i your-key.pem ubuntu@your-ec2-ip

# 프로젝트 클론 및 설정
git clone https://github.com/dugadak/MoodCare-AI.git
cd MoodCare-AI

# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Docker Compose 실행
sudo docker-compose -f docker-compose.prod.yml up -d

# Nginx 설정
sudo apt install nginx
sudo cp nginx.conf /etc/nginx/sites-available/moodcare
sudo ln -s /etc/nginx/sites-available/moodcare /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### GitHub Actions CI/CD

`.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to EC2
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ubuntu
          key: ${{ secrets.EC2_KEY }}
          script: |
            cd /home/ubuntu/MoodCare-AI
            git pull origin main
            docker-compose -f docker-compose.prod.yml down
            docker-compose -f docker-compose.prod.yml up -d --build
```

## 📁 프로젝트 구조

```
MoodCare-AI/
├── backend/
│   ├── moodcare/
│   │   ├── settings/
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── auth/
│   │   ├── emotions/
│   │   ├── stories/
│   │   └── music/
│   ├── core/
│   │   ├── ai_services/
│   │   ├── middleware/
│   │   └── utils/
│   ├── requirements.txt
│   └── manage.py
│
├── frontend/
│   ├── lib/
│   │   ├── main.dart
│   │   ├── config/
│   │   ├── models/
│   │   ├── providers/
│   │   ├── screens/
│   │   ├── services/
│   │   ├── widgets/
│   │   └── utils/
│   └── pubspec.yaml
│
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── nginx/
│
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── DEPLOYMENT.md
│
├── scripts/
│   ├── deploy.sh
│   ├── backup.sh
│   └── setup.sh
│
├── tests/
│   ├── backend/
│   └── frontend/
│
├── .github/
│   └── workflows/
│       ├── deploy.yml
│       └── test.yml
│
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
└── README.md
```

## 🔒 보안

- JWT 기반 인증
- Rate Limiting
- CORS 정책
- SQL Injection 방지
- XSS/CSRF 보호
- 데이터 암호화
- HTTPS 적용
- 정기 보안 업데이트

## 📈 성능 최적화

- Redis 캐싱
- 데이터베이스 인덱싱
- 이미지 최적화 (WebP)
- Lazy Loading
- Code Splitting
- CDN 활용
- 비동기 처리

## 🤝 기여 가이드

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 라이센스

MIT License - [LICENSE](LICENSE) 파일 참조

## 👥 팀

- Backend Development
- Frontend Development
- AI/ML Engineering
- UI/UX Design
- DevOps

## 📞 문의

- GitHub Issues: [https://github.com/dugadak/MoodCare-AI/issues](https://github.com/dugadak/MoodCare-AI/issues)
- Email: support@moodcare.ai

---

**MoodCare AI** - Your Intelligent Emotional Wellness Companion 💙✨