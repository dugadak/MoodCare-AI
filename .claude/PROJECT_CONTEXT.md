# MoodCare-AI Project Context

## 프로젝트 개요
- **프로젝트명**: MoodCare-AI
- **설명**: AI 기반 종합 감정케어 플랫폼
- **GitHub**: https://github.com/dugadak/MoodCare-AI
- **시작일**: 2025-08-27
- **현재 상태**: 기본 구조 구현 완료, 추가 기능 개발 중

## 기술 스택
### Backend
- Django 5.2.5
- Django REST Framework
- OpenAI GPT-4 API
- PostgreSQL / SQLite
- Redis (캐싱)
- Celery (비동기 작업)
- WebSocket (실시간 통신)

### Frontend
- Flutter 3.24+
- Provider (상태관리)
- Dio (API 통신)
- 3D 애니메이션 (flutter_3d_controller)
- Glassmorphism UI

## 핵심 기능
1. **AI 감정 분석**
   - 텍스트/음성 기반 감정 인식
   - GPT-4를 활용한 심리 분석
   - 실시간 감정 트렌드 분석

2. **인터랙티브 스토리텔링**
   - 감정 맞춤형 AI 스토리 생성
   - 대화형 게임북 시스템
   - 치유 내러티브

3. **음악 테라피**
   - 감정 기반 음악 추천
   - 오디오 시각화
   - ASMR 및 치료적 사운드

4. **3D UI/UX**
   - 맡길랩 스타일 3D 인터페이스
   - 감정 구체(Sphere) 시각화
   - 파티클 애니메이션 시스템

## 프로젝트 구조
```
MoodCare-Project/
├── moodcare-backend/     # Django 백엔드
│   ├── emotions/        # 감정 분석 앱
│   ├── stories/        # 스토리텔링 앱
│   ├── music/          # 음악 추천 앱
│   └── ai_analysis/    # AI 서비스
├── moodcare_app/        # Flutter 프론트엔드
│   └── lib/
│       ├── screens/    # 화면 컴포넌트
│       ├── widgets/    # 커스텀 위젯
│       └── services/   # API 서비스
└── .claude/            # 프로젝트 컨텍스트
```

## 현재 작업 상태
### 완료된 작업 ✅
- [x] GitHub 레포지토리 생성
- [x] 상세 README 문서 작성
- [x] AI 감정 분석 모듈 구현 (`emotions/ai_analyzer.py`)
- [x] 스토리텔링 모델 설계 (`stories/models.py`)
- [x] 음악 추천 시스템 모델 (`music/models.py`)
- [x] 3D UI 홈 스크린 구현
- [x] 감정 구체 위젯 개발
- [x] Emotions API serializers 구현
- [x] Stories serializers 및 AI generator 구현

### 진행 중 🔄
- [ ] Music API views 구현
- [ ] URL 라우팅 설정
- [ ] API 엔드포인트 테스트
- [ ] Flutter API 서비스 클래스
- [ ] 추가 UI 화면 개발
- [ ] WebSocket 실시간 통신

### 예정된 작업 📋
- [ ] 사용자 인증 시스템
- [ ] 푸시 알림
- [ ] 데이터 분석 대시보드
- [ ] 프리미엄 기능
- [ ] AWS 배포

## API 엔드포인트 요약
```
# 인증
POST /api/v1/auth/register
POST /api/v1/auth/login

# 감정 분석
POST /api/v1/emotions/analyze/text
POST /api/v1/emotions/analyze/voice
GET  /api/v1/emotions/records
GET  /api/v1/emotions/statistics

# 스토리
POST /api/v1/stories/generate
GET  /api/v1/stories
POST /api/v1/stories/{id}/interact

# 음악
GET  /api/v1/music/recommendations
POST /api/v1/music/playlists
```

## 환경 설정
### 필수 환경변수
```bash
SECRET_KEY=django-secret-key
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...
REDIS_URL=redis://localhost:6379
SPOTIFY_CLIENT_ID=...
SPOTIFY_CLIENT_SECRET=...
```

### 로컬 실행 명령
```bash
# Backend
cd moodcare-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend
cd moodcare_app
flutter pub get
flutter run
```

## 주요 디자인 결정
1. **3D UI 채택 이유**: 맡길랩과 토스의 혁신적 UX 참고
2. **Django 선택**: 빠른 개발과 확장성
3. **Flutter 선택**: 크로스플랫폼 지원
4. **GPT-4 활용**: 고급 감정 분석 능력

## 참고 자료
- 맡길랩 앱 UI/UX
- 토스 3D 애니메이션
- Material Design 3
- Glassmorphism 디자인 트렌드

## 다음 세션 시작 가이드
```
이 프로젝트를 계속 진행하려면:
1. 이 문서의 내용을 확인
2. 현재 작업 상태 파악
3. 진행 중/예정된 작업 선택
4. 프로젝트 구조와 기술 스택 준수
```

## 커밋 규칙
- feat: 새로운 기능
- fix: 버그 수정
- docs: 문서 수정
- style: 코드 포맷팅
- refactor: 코드 리팩토링
- test: 테스트 코드
- chore: 빌드 업무 수정

## 중요 참고사항
- Claude 관련 내용은 커밋에서 제외
- 사용자 요구사항 우선 반영
- 혁신적이고 독창적인 기능 구현 지향
- 세부 기능까지 신경써서 구현

---
Last Updated: 2025-08-27