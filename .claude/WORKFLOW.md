# MoodCare-AI 작업 플로우

## 현재 진행 상황 (2025-08-27)

### ✅ 완료된 작업
1. **프로젝트 초기 설정**
   - GitHub 레포지토리 생성
   - Django 백엔드 구조 설정
   - Flutter 프론트엔드 초기화

2. **핵심 모델 구현**
   - `emotions/ai_analyzer.py` - AI 감정 분석 엔진
   - `stories/models.py` - 스토리텔링 데이터 모델
   - `music/models.py` - 음악 추천 시스템 모델

3. **3D UI 구현**
   - `home_screen.dart` - 메인 화면 (3D 효과)
   - `emotion_sphere.dart` - 감정 구체 위젯
   - Glassmorphism UI 적용
   - 파티클 애니메이션 시스템

4. **문서화**
   - 상세 README.md
   - API 엔드포인트 문서
   - 프로젝트 컨텍스트 파일

### 🔄 진행 중인 작업
- [x] Emotions API serializers 구현 완료
- [x] Emotions views 기본 구조 업데이트
- [x] Stories serializers 구현 완료
- [x] Stories AI generator 구현 완료
- [x] Music serializers 구현 완료
- [x] Music recommender 엔진 구현 완료
- [x] URL 라우팅 설정 완료
- [ ] Music views 구현 필요
- [ ] Stories views 구현 필요
- [ ] Authentication system 구현 필요
- [ ] Flutter-Django 연동
- [ ] WebSocket 실시간 통신

### 📋 다음 단계 작업

#### Phase 1: 백엔드 완성 (1-2일)
```python
# 1. Django Views 구현
emotions/views.py
stories/views.py  
music/views.py

# 2. Serializers 생성
emotions/serializers.py
stories/serializers.py
music/serializers.py

# 3. URL 라우팅
moodcare/urls.py
emotions/urls.py
stories/urls.py
music/urls.py

# 4. 인증 시스템
users/authentication.py
```

#### Phase 2: API 연동 (1일)
```dart
// Flutter 서비스 구현
lib/services/
  - api_service.dart
  - auth_service.dart
  - emotion_service.dart
  - story_service.dart
  - music_service.dart
```

#### Phase 3: UI 화면 완성 (2-3일)
```dart
lib/screens/
  - login_screen.dart
  - emotion_record_screen.dart
  - story_screen.dart
  - music_therapy_screen.dart
  - insights_screen.dart
  - profile_screen.dart
```

#### Phase 4: 고급 기능 (2-3일)
- WebSocket 실시간 통신
- 음성 녹음 및 분석
- 3D 시각화 강화
- 오프라인 모드

#### Phase 5: 테스트 및 최적화 (1-2일)
- 유닛 테스트
- 통합 테스트
- 성능 최적화
- 보안 검토

#### Phase 6: 배포 준비 (1일)
- Docker 설정
- CI/CD 파이프라인
- AWS 인프라 구성
- 환경변수 설정

## 명령어 체크리스트

### Django 개발
```bash
# 모델 마이그레이션
python manage.py makemigrations
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser

# 테스트 실행
python manage.py test

# 서버 실행
python manage.py runserver 0.0.0.0:8000
```

### Flutter 개발
```bash
# 의존성 설치
flutter pub get

# 앱 실행
flutter run

# 빌드
flutter build apk
flutter build ios

# 테스트
flutter test
```

### Git 작업
```bash
# 현재 상태 확인
git status

# 변경사항 추가
git add .

# 커밋 (Claude 참조 제외)
git commit -m "feat: [기능 설명]"

# 푸시
git push origin main
```

## 파일 트리 구조
```
MoodCare-Project/
├── .claude/                    # 프로젝트 컨텍스트
│   ├── PROJECT_CONTEXT.md     # 프로젝트 상태
│   ├── PROMPTS.md             # 재사용 프롬프트
│   └── WORKFLOW.md            # 작업 플로우 (현재 파일)
│
├── moodcare-backend/          # Django 백엔드
│   ├── moodcare/              # 프로젝트 설정
│   ├── emotions/              # 감정 분석 앱
│   │   ├── ai_analyzer.py    ✅
│   │   ├── models.py         ✅
│   │   ├── views.py          ⏳
│   │   └── serializers.py    ⏳
│   ├── stories/               # 스토리텔링 앱
│   │   ├── models.py         ✅
│   │   ├── views.py          ⏳
│   │   └── ai_generator.py   ⏳
│   ├── music/                 # 음악 추천 앱
│   │   ├── models.py         ✅
│   │   ├── views.py          ⏳
│   │   └── recommender.py    ⏳
│   └── users/                 # 사용자 관리
│       └── models.py         ✅
│
└── moodcare_app/              # Flutter 프론트엔드
    └── lib/
        ├── main.dart          ✅
        ├── screens/
        │   ├── home_screen.dart ✅
        │   └── ...           ⏳
        ├── widgets/
        │   ├── emotion_sphere.dart ✅
        │   └── ...           ⏳
        └── services/         ⏳

Legend: ✅ 완료 | ⏳ 진행 필요 | 🔄 진행 중
```

## 브랜치 전략
```
main (production)
├── develop
    ├── feature/emotion-api
    ├── feature/story-system
    ├── feature/music-therapy
    └── feature/3d-ui
```

## 이슈 트래킹
GitHub Issues에서 관리:
- `enhancement`: 새 기능
- `bug`: 버그 수정
- `documentation`: 문서화
- `optimization`: 최적화

## 중요 결정 사항 로그
1. **2025-08-27**: GPT-4 API 사용 결정
2. **2025-08-27**: 3D UI 라이브러리 선택 (flutter_3d_controller)
3. **2025-08-27**: WebSocket 실시간 통신 채택

## 다음 세션 시작 시
1. 이 파일 읽기: `.claude/WORKFLOW.md`
2. 컨텍스트 확인: `.claude/PROJECT_CONTEXT.md`
3. 진행 중인 작업 확인
4. 해당 Phase 작업 계속

---
Last Updated: 2025-08-27
Next Action: API Views 구현