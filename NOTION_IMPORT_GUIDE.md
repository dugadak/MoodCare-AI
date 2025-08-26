# Notion 문서 가져오기 가이드

## 📌 현재 상황
- Notion API 토큰 인증 문제 발생
- MoodCare 프로젝트 문서는 로컬에 준비 완료

## 📁 준비된 문서
1. **PROJECT_PLAN.md** - 기본 프로젝트 계획서
2. **DETAILED_PLAN.md** - 상세 기획서 (10개 섹션, 완전한 문서)
3. **NOTION_DOCUMENT.html** - Notion 스타일로 포맷된 HTML 문서

## 🔧 Notion에 수동으로 가져오는 방법

### 방법 1: HTML 파일 사용 (추천)
1. 브라우저에서 `/Users/leebang/Work/MoodCare-Project/NOTION_DOCUMENT.html` 파일 열기
2. 전체 내용 선택 (Cmd+A)
3. 복사 (Cmd+C)
4. Notion에서 새 페이지 생성
5. 붙여넣기 (Cmd+V)
6. Notion이 자동으로 포맷 변환

### 방법 2: Markdown 파일 직접 임포트
1. Notion에서 새 페이지 생성
2. 우측 상단 ••• 메뉴 클릭
3. Import → Markdown 선택
4. `DETAILED_PLAN.md` 파일 선택
5. 자동 변환 완료

### 방법 3: 텍스트 직접 복사
1. `DETAILED_PLAN.md` 파일을 텍스트 에디터로 열기
2. 전체 내용 복사
3. Notion에 붙여넣기
4. Notion이 Markdown 형식 자동 인식

## 🚨 삭제해야 할 GitHub 레포지토리
- https://github.com/dugadak/moodcare-api
- https://github.com/dugadak/moodcare-app

브라우저에서 각 레포지토리 → Settings → Danger Zone → Delete this repository

## ✅ 문서 내용 검증
작성된 문서에는 다음 내용이 포함되어 있습니다:

### 상세 기획서 (DETAILED_PLAN.md)
1. **서비스 개요** - 비전, 미션, 타겟 사용자, 가치 제안
2. **상세 기능 명세** - 감정 기록, AI 분석, 추천 시스템, 커뮤니티
3. **기술 아키텍처** - 시스템 구조, DB 설계, API 설계
4. **UI/UX 디자인** - 디자인 원칙, 색상 팔레트, 화면 플로우
5. **개발 로드맵** - MVP, Beta, 정식 출시 일정
6. **비즈니스 모델** - 수익 모델, 마케팅 전략
7. **성과 측정** - KPI, 분석 도구
8. **리스크 관리** - 기술적, 규제, 비즈니스 리스크
9. **팀 구성** - 초기 팀, 확장 계획
10. **예산 계획** - 초기 투자, 손익분기점

### HTML 문서 (NOTION_DOCUMENT.html)
- Notion 스타일로 포맷된 완전한 문서
- 토글, 테이블, 콜아웃 등 Notion UI 요소 포함
- 색상 코드, 진행률 바 등 시각적 요소 구현

## 📝 다음 단계
1. Notion에 문서 임포트
2. GitHub 레포지토리 삭제
3. 실제 개발 시작:
   - API 서버 구축 (FastAPI)
   - Flutter 앱 개발
   - AI 모델 통합