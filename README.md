# 🌟 MoodCare - AI 감정케어 앱

## 📋 프로젝트 개요

MoodCare는 AI 기술을 활용하여 사용자의 감정을 분석하고 맞춤형 케어 솔루션을 제공하는 종합 정신 건강 관리 애플리케이션입니다.

### 주요 특징
- 📝 **감정 기록**: 일일 감정 체크인 및 상세 일기 작성
- 🤖 **AI 분석**: GPT-4 기반 감정 패턴 분석
- 📊 **통계 대시보드**: 감정 트렌드 시각화
- 🎯 **맞춤 추천**: 개인화된 활동 및 콘텐츠 추천

## 🛠 기술 스택

### Backend (Django)
- **Framework**: Django 5.2.5 + Django REST Framework
- **Database**: SQLite (개발) / PostgreSQL (운영)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **CORS**: django-cors-headers
- **AI**: OpenAI GPT-4 API

### Frontend (Flutter)
- **Framework**: Flutter 3.x
- **State Management**: Provider
- **Navigation**: go_router
- **HTTP**: dio, http
- **UI Components**: Material Design 3

### Infrastructure
- **Server**: AWS EC2 (프리티어)
- **CI/CD**: GitHub Actions
- **Process Manager**: tmux (백그라운드 실행)
- **Deployment**: 무중단 배포

## 🚀 Quick Start

### 필수 요구사항
- Python 3.10+
- Flutter 3.0+
- Git

### Backend 설정

```bash
# 1. 프로젝트 클론
git clone https://github.com/yourusername/moodcare.git
cd moodcare/moodcare-backend

# 2. 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경 변수 설정
cp .env.example .env
# .env 파일 편집하여 필요한 값 설정

# 5. 데이터베이스 마이그레이션
python manage.py makemigrations
python manage.py migrate

# 6. 슈퍼유저 생성
python manage.py createsuperuser

# 7. 개발 서버 실행
python manage.py runserver
```

### Frontend 설정

```bash
# 1. Flutter 프로젝트로 이동
cd ../moodcare_app

# 2. 의존성 설치
flutter pub get

# 3. API 주소 설정
# lib/services/api_service.dart 파일에서 baseUrl 수정
# 로컬: http://localhost:8000/api
# 프로덕션: http://your-ec2-ip:8000/api

# 4. 앱 실행
flutter run
```

## 📱 주요 기능

### 1. 사용자 인증
- 회원가입 / 로그인 / 로그아웃
- JWT 토큰 기반 인증
- 프로필 관리

### 2. 감정 기록
- 8가지 기본 감정 선택 (기쁨, 슬픔, 분노, 두려움, 놀람, 혐오, 신뢰, 기대)
- 감정 강도 설정 (1-10)
- 컨텍스트 정보 (장소, 활동, 날씨 등)
- 메모 및 일기 작성

### 3. 통계 및 분석
- 감정 분포 차트
- 평균 감정 강도
- 시간별 트렌드
- AI 기반 패턴 분석

### 4. AI 기능
- 감정 패턴 인식
- 트리거 분석
- 맞춤형 조언 제공

## 🔗 API 엔드포인트

### 인증
| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/users/register/` | 회원가입 |
| POST | `/api/users/login/` | 로그인 |
| POST | `/api/users/logout/` | 로그아웃 |
| POST | `/api/users/token/refresh/` | 토큰 갱신 |
| GET/PUT | `/api/users/profile/` | 프로필 조회/수정 |

### 감정 기록
| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/api/emotions/` | 감정 목록 조회 |
| POST | `/api/emotions/` | 감정 기록 생성 |
| GET/PUT/DELETE | `/api/emotions/{id}/` | 감정 상세 조회/수정/삭제 |
| GET | `/api/emotions/stats/` | 감정 통계 조회 |

## 🚢 배포

### AWS EC2 설정

```bash
# 1. EC2 인스턴스 접속
ssh -i /Users/leebang/Work/server_info/server_key/public_key.pem ubuntu@your-ec2-ip

# 2. 필수 패키지 설치
sudo apt update
sudo apt install python3-pip python3-venv nginx tmux git

# 3. 프로젝트 클론
git clone https://github.com/yourusername/moodcare.git
cd moodcare/moodcare-backend

# 4. 가상환경 설정
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. 환경 변수 설정
cp .env.example .env
nano .env  # 프로덕션 환경에 맞게 설정

# 6. Static 파일 수집
python manage.py collectstatic

# 7. tmux로 백그라운드 실행
tmux new -s moodcare
python manage.py runserver 0.0.0.0:8000

# tmux 세션 분리: Ctrl+B, D
# tmux 세션 재접속: tmux attach -t moodcare
```

### GitHub Actions CI/CD

`.github/workflows/deploy.yml` 파일이 자동으로 다음 작업을 수행합니다:
- main 브랜치 push/PR 시 자동 배포
- 테스트 실행
- EC2 서버에 자동 배포
- 무중단 배포

## 📁 프로젝트 구조

```
MoodCare-Project/
├── moodcare-backend/          # Django 백엔드
│   ├── moodcare/             # 프로젝트 설정
│   ├── users/                # 사용자 앱
│   ├── emotions/             # 감정 기록 앱
│   ├── ai_analysis/          # AI 분석 앱
│   ├── requirements.txt      # Python 의존성
│   └── manage.py            # Django 관리 스크립트
│
├── moodcare_app/             # Flutter 앱
│   ├── lib/
│   │   ├── main.dart        # 앱 진입점
│   │   ├── models/          # 데이터 모델
│   │   ├── providers/       # 상태 관리
│   │   ├── screens/         # 화면 컴포넌트
│   │   ├── services/        # API 서비스
│   │   └── widgets/         # 재사용 위젯
│   └── pubspec.yaml         # Flutter 의존성
│
└── .github/
    └── workflows/
        └── deploy.yml        # GitHub Actions CI/CD
```

## 🧪 테스트

### Backend 테스트
```bash
cd moodcare-backend
python manage.py test
```

### Frontend 테스트
```bash
cd moodcare_app
flutter test
```

## 📝 환경 변수

### Backend (.env)
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,your-ec2-ip
DATABASE_URL=postgresql://user:password@localhost/moodcare
OPENAI_API_KEY=sk-your-openai-key
JWT_ACCESS_TOKEN_LIFETIME=30
JWT_REFRESH_TOKEN_LIFETIME=7
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://your-domain.com
```

## 🔒 보안 고려사항

- JWT 토큰 기반 인증
- CORS 설정으로 허가된 도메인만 접근
- 환경 변수로 민감한 정보 관리
- HTTPS 적용 권장 (프로덕션)
- SQL Injection 방지 (Django ORM)
- XSS 공격 방지

## 🤝 기여 방법

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이센스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 👨‍💻 개발팀

- Backend Developer
- Frontend Developer
- DevOps Engineer

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.

---

**MoodCare** - Your AI Emotional Wellness Companion 💙