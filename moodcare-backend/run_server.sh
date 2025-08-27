#!/bin/bash

# MoodCare Backend Server 실행 스크립트
# Usage: ./run_server.sh

echo "🚀 MoodCare Backend 서버 시작..."

# 가상환경 활성화
if [ -d "venv" ]; then
    echo "✅ 가상환경 활성화..."
    source venv/bin/activate
else
    echo "❌ 가상환경이 없습니다. 생성 중..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 필수 패키지 설치..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# 환경 변수 확인
if [ ! -f ".env" ]; then
    echo "⚠️  .env 파일이 없습니다. .env.example을 복사합니다..."
    cp .env.example .env
    echo "📝 .env 파일을 수정해주세요 (API 키 등)"
fi

# 데이터베이스 마이그레이션
echo "🗄️  데이터베이스 마이그레이션 확인..."
python manage.py makemigrations
python manage.py migrate

# 슈퍼유저 생성 체크
echo "👤 슈퍼유저 확인..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0 if User.objects.filter(is_superuser=True).exists() else 1)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "슈퍼유저가 없습니다. 생성하시겠습니까? (y/n)"
    read -r response
    if [ "$response" = "y" ]; then
        python manage.py createsuperuser
    fi
fi

# 정적 파일 수집 (프로덕션용)
if [ "$DEBUG" = "False" ]; then
    echo "📁 정적 파일 수집..."
    python manage.py collectstatic --noinput
fi

# 서버 실행
echo "🌟 서버 시작 (http://127.0.0.1:8000/)"
echo "📚 API 문서: http://127.0.0.1:8000/api/v1/"
echo "🔐 Admin: http://127.0.0.1:8000/admin/"
echo "종료: Ctrl+C"
echo "================================"

python manage.py runserver 0.0.0.0:8000