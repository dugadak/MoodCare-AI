# MoodCare-AI 프롬프트 템플릿

## 프로젝트 재개 프롬프트
```
MoodCare-AI 프로젝트를 계속 진행해줘.
프로젝트 경로: /Users/leebang/Work/MoodCare-Project
GitHub: https://github.com/dugadak/MoodCare-AI
.claude/PROJECT_CONTEXT.md 파일을 참고해서 이어서 작업해줘.
```

## 주요 기능 개발 프롬프트

### 1. AI 감정 분석 강화
```
MoodCare 프로젝트의 AI 감정 분석 기능을 더 고도화해줘:
1. 멀티모달 감정 인식 (텍스트+음성+표정)
2. 실시간 감정 변화 추적
3. 감정 예측 모델
4. 개인화된 감정 패턴 학습
```

### 2. 3D UI 개선
```
맡길랩과 토스 앱처럼 혁신적인 3D UI를 추가로 구현해줘:
1. 3D 카드 플립 애니메이션
2. 파티클 시스템 강화
3. 모션 블러 효과
4. 다이나믹 테마 변경
5. 햅틱 피드백 최적화
```

### 3. 스토리텔링 시스템
```
인터랙티브 스토리텔링 기능을 구현해줘:
1. GPT-4 기반 스토리 생성
2. 사용자 선택에 따른 분기
3. 감정 상태 반영 스토리
4. 음성 나레이션 추가
5. 일러스트 자동 생성
```

### 4. 음악 테라피
```
음악 추천 및 테라피 기능을 구현해줘:
1. Spotify API 연동
2. 감정별 플레이리스트 생성
3. 바이노럴 비트 생성
4. 오디오 시각화 (3D)
5. 음악 일기 기능
```

### 5. 실시간 기능
```
WebSocket을 활용한 실시간 기능 구현:
1. 실시간 감정 분석 피드백
2. 라이브 감정 공유
3. 그룹 테라피 세션
4. 실시간 음악 동기화
```

## API 개발 프롬프트

### Django API 엔드포인트
```
다음 API 엔드포인트를 Django REST Framework로 구현해줘:
- POST /api/v1/emotions/analyze/multimodal
- GET /api/v1/emotions/predictions
- POST /api/v1/stories/generate
- GET /api/v1/music/therapy/{emotion}
- WebSocket /ws/emotions/live
```

### Flutter API 연동
```
Flutter에서 Django API와 연동하는 서비스 클래스 만들어줘:
1. Dio를 사용한 HTTP 통신
2. JWT 토큰 관리
3. 에러 핸들링
4. 오프라인 모드 지원
5. 캐싱 전략
```

## UI/UX 구현 프롬프트

### 감정 시각화
```
감정 상태를 3D로 시각화하는 위젯 만들어줘:
1. 감정 구체 (Emotion Sphere)
2. 감정 파티클 시스템
3. 색상 그라데이션 애니메이션
4. 인터랙티브 터치 반응
```

### 화면 전환 애니메이션
```
맡길랩처럼 부드러운 화면 전환 애니메이션 구현:
1. Hero 애니메이션
2. 페이지 라우트 트랜지션
3. 공유 요소 전환
4. 물리 기반 애니메이션
```

## 테스트 프롬프트

### 단위 테스트
```
다음 기능들의 단위 테스트 작성:
1. EmotionAnalyzer 클래스
2. StoryGenerator 서비스
3. MusicRecommender 알고리즘
4. API 엔드포인트 테스트
```

### 통합 테스트
```
전체 플로우 통합 테스트:
1. 사용자 등록 → 로그인
2. 감정 기록 → 분석
3. 스토리 생성 → 저장
4. 음악 추천 → 재생
```

## 배포 프롬프트

### AWS 배포
```
MoodCare 프로젝트를 AWS에 배포:
1. EC2 인스턴스 설정
2. RDS PostgreSQL 설정
3. S3 미디어 스토리지
4. CloudFront CDN
5. GitHub Actions CI/CD
```

### Docker 컨테이너화
```
프로젝트를 Docker로 컨테이너화:
1. Django Dockerfile
2. Flutter Web Dockerfile
3. docker-compose.yml
4. 환경변수 설정
```

## 디버깅 프롬프트
```
다음 오류를 해결해줘:
[오류 메시지 붙여넣기]
프로젝트 경로: /Users/leebang/Work/MoodCare-Project
```

## 코드 리뷰 프롬프트
```
MoodCare 프로젝트의 다음 코드를 리뷰하고 개선점 제안:
1. 성능 최적화
2. 보안 취약점
3. 코드 품질
4. 베스트 프랙티스
```

## 문서화 프롬프트
```
MoodCare 프로젝트의 다음 문서 작성:
1. API 문서 (Swagger)
2. 사용자 가이드
3. 개발자 문서
4. 배포 가이드
```

---

## 사용 방법
1. 새 Claude 세션 시작
2. 프로젝트 재개 프롬프트 입력
3. PROJECT_CONTEXT.md 확인 요청
4. 필요한 작업 프롬프트 선택 및 실행

## 주의사항
- Claude 관련 내용은 커밋에서 제외
- 프로젝트 컨텍스트 파일 정기적 업데이트
- 각 세션 종료 시 진행 상황 저장