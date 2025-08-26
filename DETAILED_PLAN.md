# 🌟 MoodCare - AI 감정케어 앱 상세 기획서

## 1. 서비스 개요

### 1.1 서비스명
**MoodCare (무드케어)** - Your AI Emotional Wellness Companion

### 1.2 비전
"모든 사람이 건강한 감정 생활을 영위할 수 있는 세상"

### 1.3 미션
- AI 기술을 활용한 접근 가능한 정신 건강 케어 제공
- 일상 속 감정 관리를 통한 삶의 질 향상
- 데이터 기반 개인 맞춤형 감정 케어 솔루션 제공

### 1.4 타겟 사용자

#### 주요 타겟 (Primary Target)
- **20-30대 직장인**
  - 스트레스 관리가 필요한 사람
  - 바쁜 일상으로 정신 건강 관리가 어려운 사람
  - 디지털 서비스에 익숙한 세대

#### 보조 타겟 (Secondary Target)
- **대학생 및 취업 준비생**
  - 진로 고민과 스트레스를 겪는 사람
  - 경제적 부담으로 전문 상담이 어려운 사람

- **주부 및 육아맘**
  - 육아 스트레스와 고립감을 느끼는 사람
  - 시간적 제약으로 외부 활동이 어려운 사람

### 1.5 핵심 가치 제안 (Value Proposition)

1. **접근성**: 언제 어디서나 이용 가능한 24/7 감정 케어
2. **개인화**: AI 기반 맞춤형 분석과 추천
3. **익명성**: 안전하고 비밀이 보장되는 감정 표현 공간
4. **전문성**: 검증된 심리학 이론과 AI 기술의 결합
5. **경제성**: 전문 상담 대비 합리적인 비용

## 2. 상세 기능 명세

### 2.1 감정 기록 시스템

#### 2.1.1 Quick Mood Check-in
**목적**: 빠르고 간편한 일일 감정 기록

**기능 상세**:
- **감정 휠 (Emotion Wheel)**
  - Plutchik의 감정 휠 기반 8가지 기본 감정
  - 각 감정별 3단계 강도 선택
  - 복합 감정 선택 가능

- **컨텍스트 태깅**
  - 장소: 집, 직장, 학교, 야외, 기타
  - 활동: 일, 휴식, 운동, 식사, 대화, 기타
  - 사람: 혼자, 가족, 친구, 동료, 기타
  - 날씨: 맑음, 흐림, 비, 눈
  - 신체 상태: 피곤함, 활력, 아픔, 보통

- **빠른 메모**
  - 200자 이내 간단 메모
  - 음성 메모 (최대 1분)
  - 사진 첨부 (최대 3장)

#### 2.1.2 감정 일기 (Emotion Journal)
**목적**: 깊이 있는 감정 탐색과 기록

**기능 상세**:
- **가이드 질문**
  - "오늘 가장 강렬했던 감정은?"
  - "그 감정을 느낀 계기는?"
  - "몸의 어느 부분에서 감정을 느꼈나요?"
  - "이 감정이 당신에게 전하는 메시지는?"

- **자유 작성**
  - 제한 없는 텍스트 입력
  - 리치 텍스트 에디터 (굵기, 기울임, 밑줄)
  - 이모지 지원

- **AI 분석 피드백**
  - 감정 키워드 추출
  - 감정 톤 분석 (긍정/부정/중립)
  - 인지 왜곡 패턴 감지

#### 2.1.3 음성 감정 분석
**목적**: 음성을 통한 감정 상태 파악

**기능 상세**:
- **음성 녹음**
  - 최대 5분 녹음
  - 백그라운드 노이즈 제거
  
- **분석 요소**
  - 음성 톤과 피치
  - 말하기 속도
  - 감정 어휘 사용 빈도
  - STT 후 텍스트 감정 분석

### 2.2 AI 기반 분석 엔진

#### 2.2.1 감정 패턴 분석
**목적**: 장기적 감정 변화 패턴 파악

**분석 항목**:
- **시간대별 패턴**
  - 요일별 감정 변화
  - 시간대별 감정 분포
  - 계절별 감정 트렌드

- **트리거 분석**
  - 반복되는 감정 트리거 식별
  - 트리거-감정 상관관계
  - 대처 방식 효과성 분석

- **감정 사이클**
  - 감정 주기 파악
  - 예측 가능한 패턴 알림
  - 사전 대비 추천

#### 2.2.2 AI 챗봇 (MoodBot)
**목적**: 24/7 감정 지원 및 상담

**대화 시나리오**:
1. **초기 응답**
   - 공감적 인사
   - 현재 감정 확인
   - 대화 희망 여부 확인

2. **심화 대화**
   - 개방형 질문
   - 반영적 경청
   - 감정 검증

3. **솔루션 제안**
   - 즉시 실천 가능한 활동
   - 장기적 개선 방안
   - 전문가 연계 안내

**AI 모델**:
- Base Model: GPT-4 Fine-tuned
- 한국어 감정 어휘 특화 학습
- CBT, DBT 기법 통합

#### 2.2.3 개인화 추천 시스템
**목적**: 사용자별 맞춤 콘텐츠 제공

**추천 알고리즘**:
- **협업 필터링**
  - 유사 사용자 패턴 분석
  - 효과적인 개입 방법 공유

- **콘텐츠 기반 필터링**
  - 과거 선호도 분석
  - 효과성 피드백 반영

- **하이브리드 접근**
  - 상황별 가중치 조정
  - 실시간 감정 상태 반영

### 2.3 웰니스 콘텐츠

#### 2.3.1 명상 & 마음챙김
**콘텐츠 구성**:
- **가이드 명상**
  - 초급 (5분): 호흡 명상, 바디스캔
  - 중급 (10분): 자애 명상, 걷기 명상
  - 고급 (15분+): 통찰 명상, 개방 명상

- **상황별 명상**
  - 불안 완화
  - 수면 유도
  - 집중력 향상
  - 스트레스 해소

#### 2.3.2 운동 & 활동
**추천 활동**:
- **실내 운동**
  - 요가 시퀀스
  - 스트레칭
  - 간단한 유산소

- **야외 활동**
  - 산책 코스 추천
  - 자연 관찰
  - 사진 찍기 미션

#### 2.3.3 창의적 활동
**콘텐츠 유형**:
- **표현 활동**
  - 감정 그리기
  - 감정 편지 쓰기
  - 음악 플레이리스트 만들기

- **취미 활동**
  - 간단한 요리
  - 식물 가꾸기
  - 독서 추천

### 2.4 커뮤니티 기능

#### 2.4.1 익명 감정 공유
**기능 상세**:
- **포스팅**
  - 완전 익명 (랜덤 닉네임)
  - 감정 태그 필수
  - 부적절한 콘텐츠 AI 필터링

- **상호작용**
  - 공감 버튼 (하트, 허그, 응원)
  - 지지 메시지 (사전 정의 + 커스텀)
  - 신고 기능

#### 2.4.2 그룹 프로그램
**프로그램 유형**:
- **감정 관리 워크샵**
  - 주 1회, 4주 프로그램
  - 10명 이내 소그룹
  - 전문 퍼실리테이터 진행

- **또래 지원 그룹**
  - 주제별 모임 (직장 스트레스, 관계, 육아 등)
  - 정기 온라인 미팅
  - 경험 공유 및 상호 지원

### 2.5 데이터 시각화 & 리포트

#### 2.5.1 대시보드
**주요 위젯**:
- **감정 날씨**
  - 오늘의 감정을 날씨로 표현
  - 주간 날씨 예보 형식

- **감정 온도계**
  - 감정 에너지 레벨
  - 목표 대비 현재 상태

- **무드 트래커**
  - 30일 감정 히트맵
  - 감정 변화 그래프

#### 2.5.2 인사이트 리포트
**월간 리포트 구성**:
1. **요약 페이지**
   - 주요 감정 TOP 3
   - 가장 좋았던 날 / 힘들었던 날
   - 전월 대비 변화

2. **패턴 분석**
   - 감정 트리거 맵
   - 대처 전략 효과성
   - 개선 영역 제안

3. **성장 지표**
   - 감정 인식 능력
   - 회복 탄력성
   - 자기 돌봄 실천율

## 3. 기술 아키텍처

### 3.1 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                     Client Layer                         │
├─────────────────────────────────────────────────────────┤
│  Flutter App (iOS/Android)  │  Web App (React)          │
└─────────────────┬───────────┴───────────┬───────────────┘
                  │                       │
                  ▼                       ▼
┌─────────────────────────────────────────────────────────┐
│                     API Gateway                          │
│                  (Kong / AWS API Gateway)                │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                  Microservices Layer                     │
├───────────────┬─────────────┬─────────────┬─────────────┤
│ Auth Service  │ User Service│ Emotion     │ AI Service  │
│ (FastAPI)     │ (FastAPI)   │ Service     │ (FastAPI)   │
│               │             │ (FastAPI)   │             │
├───────────────┼─────────────┼─────────────┼─────────────┤
│ Community     │ Content     │ Analytics   │Notification │
│ Service       │ Service     │ Service     │ Service     │
│ (FastAPI)     │ (FastAPI)   │ (FastAPI)   │ (FastAPI)   │
└───────────────┴─────────────┴─────────────┴─────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                            │
├─────────────────────────┬────────────────────────────────┤
│   PostgreSQL (Main DB)  │    Redis (Cache/Queue)        │
├─────────────────────────┼────────────────────────────────┤
│   MongoDB (Logs)        │    S3 (Media Storage)         │
└─────────────────────────┴────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                 External Services                        │
├─────────────────────────┬────────────────────────────────┤
│   OpenAI API            │    Firebase (Push)            │
├─────────────────────────┼────────────────────────────────┤
│   SendGrid (Email)      │    Stripe (Payment)          │
└─────────────────────────┴────────────────────────────────┘
```

### 3.2 데이터베이스 설계

#### 3.2.1 핵심 테이블

**users**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    profile JSONB DEFAULT '{}',
    settings JSONB DEFAULT '{}',
    subscription_tier VARCHAR(50) DEFAULT 'free',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false
);
```

**emotions**
```sql
CREATE TABLE emotions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    emotion_type VARCHAR(50) NOT NULL,
    intensity INTEGER CHECK (intensity >= 1 AND intensity <= 10),
    sub_emotions JSONB DEFAULT '[]',
    note TEXT,
    voice_note_url VARCHAR(500),
    images JSONB DEFAULT '[]',
    context JSONB DEFAULT '{}',
    ai_analysis JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_created (user_id, created_at DESC)
);
```

**ai_conversations**
```sql
CREATE TABLE ai_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id UUID NOT NULL,
    messages JSONB NOT NULL DEFAULT '[]',
    sentiment_summary JSONB,
    recommendations JSONB DEFAULT '[]',
    effectiveness_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    INDEX idx_user_session (user_id, session_id)
);
```

**recommendations**
```sql
CREATE TABLE recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    content JSONB NOT NULL,
    trigger_emotion VARCHAR(50),
    trigger_context JSONB,
    was_helpful BOOLEAN,
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    interacted_at TIMESTAMP,
    INDEX idx_user_type (user_id, type, created_at DESC)
);
```

**community_posts**
```sql
CREATE TABLE community_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    anonymous_name VARCHAR(100) NOT NULL,
    emotion_tags JSONB NOT NULL DEFAULT '[]',
    content TEXT NOT NULL,
    support_count INTEGER DEFAULT 0,
    is_flagged BOOLEAN DEFAULT false,
    is_hidden BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created_visible (created_at DESC, is_hidden)
);
```

### 3.3 API 설계

#### 3.3.1 RESTful API Endpoints

**인증 관련**
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh
POST   /api/v1/auth/verify-email
POST   /api/v1/auth/reset-password
```

**감정 기록**
```
GET    /api/v1/emotions
POST   /api/v1/emotions
GET    /api/v1/emotions/{id}
PUT    /api/v1/emotions/{id}
DELETE /api/v1/emotions/{id}
GET    /api/v1/emotions/stats
GET    /api/v1/emotions/patterns
```

**AI 서비스**
```
POST   /api/v1/ai/chat
GET    /api/v1/ai/conversations
GET    /api/v1/ai/conversations/{id}
POST   /api/v1/ai/analyze-emotion
POST   /api/v1/ai/generate-recommendations
GET    /api/v1/ai/insights
```

**커뮤니티**
```
GET    /api/v1/community/posts
POST   /api/v1/community/posts
GET    /api/v1/community/posts/{id}
POST   /api/v1/community/posts/{id}/support
POST   /api/v1/community/posts/{id}/report
GET    /api/v1/community/groups
POST   /api/v1/community/groups/{id}/join
```

**콘텐츠**
```
GET    /api/v1/content/meditations
GET    /api/v1/content/meditations/{id}
GET    /api/v1/content/activities
GET    /api/v1/content/activities/recommended
POST   /api/v1/content/activities/{id}/complete
```

### 3.4 보안 및 개인정보 보호

#### 3.4.1 데이터 보안
- **암호화**
  - 전송 중: TLS 1.3
  - 저장 시: AES-256-GCM
  - 민감 정보: 별도 암호화 키 관리 (AWS KMS)

- **인증 및 권한**
  - JWT + Refresh Token
  - OAuth 2.0 (소셜 로그인)
  - 2FA 옵션 제공
  - Role-based Access Control

#### 3.4.2 개인정보 보호
- **데이터 최소화**
  - 필수 정보만 수집
  - 자동 데이터 만료 정책
  - 익명화/가명화 처리

- **사용자 권리**
  - 데이터 열람권
  - 수정/삭제권
  - 데이터 이동권
  - 처리 제한/거부권

- **규정 준수**
  - GDPR, CCPA 준수
  - 국내 개인정보보호법 준수
  - 정기 보안 감사

## 4. UI/UX 디자인

### 4.1 디자인 원칙

1. **Calm Technology**
   - 부드러운 색상과 애니메이션
   - 과도한 알림 지양
   - 사용자 페이스 존중

2. **Inclusive Design**
   - 다양한 감정 표현 방식 제공
   - 접근성 표준 준수 (WCAG 2.1)
   - 다국어 지원

3. **Privacy First**
   - 명확한 데이터 사용 안내
   - 세밀한 프라이버시 설정
   - 익명성 보장

### 4.2 색상 팔레트

```
Primary Colors:
- Calm Blue:    #4A90E2 (신뢰, 안정)
- Soft Purple:  #9B59B6 (창의, 영감)
- Warm Peach:   #FFB6C1 (따뜻함, 공감)

Emotion Colors:
- Joy:          #FFD700 (금색)
- Sadness:      #5DADE2 (하늘색)
- Anger:        #E74C3C (빨강)
- Fear:         #8E44AD (보라)
- Surprise:     #F39C12 (주황)
- Disgust:      #27AE60 (초록)
- Trust:        #3498DB (파랑)
- Anticipation: #E67E22 (호박색)

Neutral Colors:
- Background:   #F8F9FA
- Text Primary: #2C3E50
- Text Secondary: #7F8C8D
- Border:       #ECF0F1
```

### 4.3 타이포그래피

```
Heading Font: 'Pretendard' (한글), 'Inter' (영문)
Body Font: 'Spoqa Han Sans Neo' (한글), 'Roboto' (영문)

Font Sizes:
- H1: 32px / 48px
- H2: 24px / 36px
- H3: 20px / 30px
- Body: 16px / 24px
- Caption: 14px / 20px
- Small: 12px / 18px
```

### 4.4 주요 화면 플로우

```
1. 온보딩 플로우
   스플래시 → 소개 (3단계) → 회원가입/로그인 → 
   초기 설정 → 첫 감정 체크인 → 홈

2. 일일 체크인 플로우
   홈 → Quick Check-in → 감정 선택 → 
   컨텍스트 태깅 → 메모 (선택) → 완료 → 
   AI 피드백 → 추천 활동

3. AI 챗봇 플로우
   홈/탭바 → 챗봇 → 인사 메시지 → 
   사용자 입력 → AI 응답 → 대화 진행 → 
   세션 종료 → 요약 및 추천

4. 커뮤니티 플로우
   커뮤니티 탭 → 피드 탐색 → 포스트 상세 → 
   공감/지지 → 작성하기 → 익명 설정 → 
   공유 → 피드 반영
```

## 5. 개발 로드맵

### 5.1 MVP (Minimum Viable Product) - 8주

**Week 1-2: 프로젝트 설정**
- [ ] 개발 환경 구성
- [ ] Git 레포지토리 설정
- [ ] CI/CD 파이프라인 구축
- [ ] 기본 프로젝트 구조 생성

**Week 3-4: 백엔드 기초**
- [ ] 사용자 인증 시스템
- [ ] 감정 CRUD API
- [ ] 데이터베이스 스키마 구현
- [ ] 기본 보안 설정

**Week 5-6: 프론트엔드 기초**
- [ ] Flutter 앱 기본 구조
- [ ] 로그인/회원가입 화면
- [ ] 감정 기록 화면
- [ ] 기본 네비게이션

**Week 7-8: 통합 및 테스트**
- [ ] API 연동
- [ ] 기본 기능 테스트
- [ ] 버그 수정
- [ ] Alpha 버전 배포

### 5.2 Beta Version - 8주

**Week 9-10: AI 통합**
- [ ] OpenAI API 연동
- [ ] 감정 분석 모델 구현
- [ ] 챗봇 기본 기능
- [ ] AI 피드백 시스템

**Week 11-12: 데이터 시각화**
- [ ] 감정 차트 구현
- [ ] 대시보드 개발
- [ ] 통계 API
- [ ] 리포트 생성 기능

**Week 13-14: 콘텐츠 시스템**
- [ ] 명상 콘텐츠 통합
- [ ] 활동 추천 시스템
- [ ] 콘텐츠 관리 시스템
- [ ] 사용자 피드백 수집

**Week 15-16: 베타 테스트**
- [ ] 클로즈드 베타 테스트
- [ ] 사용자 피드백 수집
- [ ] 성능 최적화
- [ ] 버그 수정

### 5.3 정식 출시 - 4주

**Week 17-18: 커뮤니티 기능**
- [ ] 익명 포스팅 시스템
- [ ] 상호작용 기능
- [ ] 신고/관리 시스템
- [ ] 그룹 기능 기초

**Week 19-20: 최종 준비**
- [ ] 앱 스토어 최적화
- [ ] 마케팅 자료 준비
- [ ] 문서화 완성
- [ ] 프로덕션 환경 설정

**Week 21-22: 출시 및 모니터링**
- [ ] 앱 스토어 제출
- [ ] 소프트 런칭
- [ ] 실시간 모니터링
- [ ] 핫픽스 대응

## 6. 비즈니스 모델

### 6.1 수익 모델

#### Freemium Model

**Free Tier (무료)**
- 기본 감정 기록 (일 3회)
- AI 챗봇 (일 10 메시지)
- 기본 통계
- 커뮤니티 접근

**Premium Tier (월 9,900원)**
- 무제한 감정 기록
- 무제한 AI 챗봇
- 고급 분석 및 리포트
- 모든 콘텐츠 접근
- 광고 제거

**Professional Tier (월 19,900원)**
- Premium 모든 기능
- 전문가 상담 연계 (월 1회)
- 그룹 프로그램 우선 참여
- 개인 맞춤 코칭
- 데이터 export 기능

#### B2B Model
- 기업 직원 복지 프로그램
- 단체 라이선스
- 맞춤형 대시보드
- 조직 건강도 리포트

### 6.2 마케팅 전략

#### 초기 사용자 확보
1. **콘텐츠 마케팅**
   - 정신 건강 블로그
   - YouTube 채널
   - 팟캐스트

2. **파트너십**
   - 정신 건강 단체
   - 대학 상담 센터
   - 기업 HR 부서

3. **소셜 미디어**
   - Instagram 감정 일기
   - TikTok 짧은 명상
   - Twitter 일일 팁

4. **인플루언서 협업**
   - 웰니스 인플루언서
   - 정신 건강 전문가
   - 라이프스타일 크리에이터

## 7. 성과 측정

### 7.1 핵심 성과 지표 (KPIs)

#### 사용자 지표
- **획득**: 월간 신규 가입자 수
- **활성화**: 7일 내 3회 이상 사용률
- **유지**: 30일 리텐션율
- **수익**: 유료 전환율, ARPU
- **추천**: NPS Score

#### 참여도 지표
- **DAU/MAU Ratio**: 일일/월간 활성 사용자 비율
- **Session Duration**: 평균 세션 시간
- **Feature Adoption**: 기능별 사용률
- **Content Engagement**: 콘텐츠 완료율

#### 건강 성과 지표
- **Mood Improvement**: 감정 개선 지수
- **Consistency**: 연속 기록 일수
- **Community Impact**: 지지 메시지 효과
- **AI Effectiveness**: AI 추천 만족도

### 7.2 분석 도구

- **Firebase Analytics**: 앱 사용 행동 분석
- **Mixpanel**: 사용자 여정 추적
- **Amplitude**: 코호트 분석
- **Custom Dashboard**: 내부 지표 모니터링

## 8. 리스크 관리

### 8.1 기술적 리스크
- **데이터 유출**: 암호화, 정기 보안 감사
- **서버 다운**: 자동 스케일링, 다중 가용 영역
- **AI 오작동**: 휴먼 리뷰, 폴백 시스템

### 8.2 규제 리스크
- **의료 행위 규제**: 명확한 면책 조항, 전문가 자문
- **개인정보 규제**: 법무 검토, 규정 준수 체크리스트
- **콘텐츠 책임**: 사용자 생성 콘텐츠 모니터링

### 8.3 비즈니스 리스크
- **경쟁사 출현**: 지속적 혁신, 사용자 락인
- **수익성 부족**: 다양한 수익 모델, 비용 최적화
- **사용자 이탈**: 지속적 개선, 커뮤니티 강화

## 9. 팀 구성

### 9.1 핵심 팀 (초기)

- **Product Manager**: 1명
- **Backend Developer**: 2명
- **Frontend Developer**: 2명
- **AI/ML Engineer**: 1명
- **UI/UX Designer**: 1명
- **Content Creator**: 1명
- **Marketing Manager**: 1명

### 9.2 확장 계획 (6개월 후)

- **DevOps Engineer**: 1명
- **Data Analyst**: 1명
- **Community Manager**: 1명
- **Customer Success**: 2명
- **Clinical Advisor**: 1명 (파트타임)

## 10. 예산 계획

### 10.1 초기 투자 (6개월)

**개발 비용**
- 인건비: 3억원
- 인프라: 3,000만원
- 외주/툴: 2,000만원

**마케팅 비용**
- 디지털 마케팅: 5,000만원
- 콘텐츠 제작: 2,000만원
- 이벤트/PR: 3,000만원

**운영 비용**
- 사무실/관리: 3,000만원
- 법무/회계: 1,000만원
- 예비비: 2,000만원

**총 예상 비용**: 4.6억원

### 10.2 손익분기점

- 예상 시점: 출시 후 18개월
- 필요 유료 사용자: 15,000명
- 목표 전환율: 5%
- 필요 MAU: 300,000명

---

*이 문서는 MoodCare 프로젝트의 상세 기획서입니다.*
*작성일: 2025-01-25*
*버전: 1.0*