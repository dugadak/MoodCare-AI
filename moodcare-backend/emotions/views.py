from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
import json
import speech_recognition as sr
from io import BytesIO

from .models import EmotionRecord
from .serializers import (
    EmotionRecordSerializer,
    TextAnalysisSerializer,
    VoiceAnalysisSerializer,
    EmotionStatisticsSerializer,
    EmotionTrendSerializer,
    EmotionInsightSerializer
)
from .ai_analyzer import EmotionAnalyzer


class EmotionRecordViewSet(viewsets.ModelViewSet):
    """감정 기록 ViewSet"""
    serializer_class = EmotionRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['emotion_type', 'sub_emotion']
    
    def get_queryset(self):
        """사용자의 감정 기록만 반환"""
        return EmotionRecord.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        """감정 기록 생성"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def analyze_text(self, request):
        """텍스트 기반 감정 분석"""
        serializer = TextAnalysisSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        text = serializer.validated_data['text']
        situation = serializer.validated_data.get('situation', '')
        
        # AI 분석 수행
        analyzer = EmotionAnalyzer()
        analysis_result = analyzer.analyze_text(text, situation)
        
        if not analysis_result:
            return Response(
                {'error': '감정 분석에 실패했습니다.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # 감정 기록 저장
        emotion_record = EmotionRecord.objects.create(
            user=request.user,
            emotion_type=analysis_result['emotion_type'],
            sub_emotion=analysis_result.get('sub_emotion'),
            intensity=analysis_result['intensity'],
            text=text,
            ai_analysis=analysis_result.get('detailed_analysis', {}),
            triggers=analysis_result.get('triggers', []),
            physical_sensations=analysis_result.get('physical_sensations', []),
            thoughts=analysis_result.get('thoughts', []),
            situation=situation
        )
        
        # 대응 전략 추가
        response_data = EmotionRecordSerializer(emotion_record).data
        response_data['recommendations'] = analyzer.get_coping_strategies(
            analysis_result['emotion_type'],
            analysis_result['intensity']
        )
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def analyze_voice(self, request):
        """음성 기반 감정 분석"""
        serializer = VoiceAnalysisSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        audio_file = serializer.validated_data['audio_file']
        situation = serializer.validated_data.get('situation', '')
        
        try:
            # 음성을 텍스트로 변환
            recognizer = sr.Recognizer()
            audio_data = BytesIO(audio_file.read())
            
            with sr.AudioFile(audio_data) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language='ko-KR')
            
            # 텍스트 기반 분석 수행
            analyzer = EmotionAnalyzer()
            analysis_result = analyzer.analyze_voice_features(text, {
                'duration': len(audio.frame_data) / audio.sample_rate,
                'sample_rate': audio.sample_rate
            })
            
            # 감정 기록 저장
            emotion_record = EmotionRecord.objects.create(
                user=request.user,
                emotion_type=analysis_result['emotion_type'],
                sub_emotion=analysis_result.get('sub_emotion'),
                intensity=analysis_result['intensity'],
                text=text,
                ai_analysis=analysis_result,
                triggers=analysis_result.get('triggers', []),
                situation=situation,
                is_voice=True
            )
            
            response_data = EmotionRecordSerializer(emotion_record).data
            response_data['transcribed_text'] = text
            response_data['voice_features'] = analysis_result.get('voice_features', {})
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except sr.UnknownValueError:
            return Response(
                {'error': '음성을 인식할 수 없습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'음성 분석 중 오류가 발생했습니다: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """감정 통계"""
        # 기간 파라미터
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        records = self.get_queryset().filter(created_at__gte=start_date)
        
        # 기본 통계
        total_records = records.count()
        if total_records == 0:
            return Response({
                'total_records': 0,
                'emotion_distribution': {},
                'average_intensity': 0,
                'most_common_emotion': None,
                'daily_average': 0
            })
        
        # 감정 분포
        emotion_distribution = {}
        for record in records:
            emotion_distribution[record.emotion_type] = emotion_distribution.get(record.emotion_type, 0) + 1
        
        # 평균 강도
        average_intensity = records.aggregate(Avg('intensity'))['intensity__avg']
        
        # 가장 흔한 감정
        most_common_emotion = max(emotion_distribution.items(), key=lambda x: x[1])
        
        # 일별 평균
        daily_average = total_records / max(days, 1)
        
        # 시간대별 분포
        hourly_distribution = {}
        for hour in range(24):
            count = records.filter(created_at__hour=hour).count()
            hourly_distribution[f"{hour:02d}:00"] = count
        
        # 트리거 분석
        all_triggers = []
        for record in records:
            all_triggers.extend(record.triggers or [])
        
        trigger_frequency = {}
        for trigger in all_triggers:
            trigger_frequency[trigger] = trigger_frequency.get(trigger, 0) + 1
        
        return Response({
            'total_records': total_records,
            'emotion_distribution': emotion_distribution,
            'average_intensity': round(average_intensity or 0, 2),
            'most_common_emotion': most_common_emotion[0] if most_common_emotion else None,
            'daily_average': round(daily_average, 2),
            'hourly_distribution': hourly_distribution,
            'top_triggers': sorted(trigger_frequency.items(), key=lambda x: x[1], reverse=True)[:5],
            'period_days': days
        })
    
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """감정 트렌드 분석"""
        days = int(request.query_params.get('days', 7))
        
        trends = []
        for i in range(days):
            date = timezone.now().date() - timedelta(days=i)
            records = self.get_queryset().filter(
                created_at__date=date
            )
            
            if records.exists():
                daily_data = {
                    'date': date.isoformat(),
                    'record_count': records.count(),
                    'average_intensity': records.aggregate(Avg('intensity'))['intensity__avg'],
                    'dominant_emotion': records.values('emotion_type').annotate(
                        count=Count('id')
                    ).order_by('-count').first()
                }
                trends.append(daily_data)
        
        # 주간 패턴 분석
        weekly_pattern = []
        for day in range(7):
            day_name = ['월', '화', '수', '목', '금', '토', '일'][day]
            day_records = self.get_queryset().filter(
                created_at__week_day=(day + 2) % 7 + 1  # Django week_day는 일요일이 1
            )
            
            if day_records.exists():
                weekly_pattern.append({
                    'day': day_name,
                    'average_intensity': day_records.aggregate(Avg('intensity'))['intensity__avg'],
                    'record_count': day_records.count()
                })
        
        return Response({
            'daily_trends': trends,
            'weekly_pattern': weekly_pattern,
            'trend_direction': self._calculate_trend_direction(trends)
        })
    
    @action(detail=False, methods=['get'])
    def insights(self, request):
        """AI 기반 감정 인사이트"""
        records = self.get_queryset()[:100]  # 최근 100개 기록
        
        if not records:
            return Response({'insights': [], 'patterns': []})
        
        analyzer = EmotionAnalyzer()
        
        # 패턴 분석
        patterns = []
        emotion_sequences = [r.emotion_type for r in records]
        
        # 반복 패턴 찾기
        for i in range(len(emotion_sequences) - 2):
            pattern = emotion_sequences[i:i+3]
            if emotion_sequences.count(pattern) > 1:
                patterns.append({
                    'sequence': pattern,
                    'frequency': emotion_sequences.count(pattern)
                })
        
        # AI 인사이트 생성
        recent_emotions = [(r.emotion_type, r.intensity) for r in records[:10]]
        insights = analyzer.generate_insights(recent_emotions)
        
        # 개선 제안
        recommendations = []
        negative_count = sum(1 for r in records[:30] if r.emotion_type in ['sad', 'angry', 'anxious', 'stressed'])
        
        if negative_count > 15:
            recommendations.append({
                'type': 'warning',
                'message': '최근 부정적인 감정이 자주 기록되고 있습니다.',
                'suggestion': '명상이나 운동 등의 스트레스 해소 활동을 권장합니다.'
            })
        
        positive_count = sum(1 for r in records[:30] if r.emotion_type in ['happy', 'excited', 'grateful', 'peaceful'])
        if positive_count > 20:
            recommendations.append({
                'type': 'celebration',
                'message': '긍정적인 감정 상태를 잘 유지하고 있습니다!',
                'suggestion': '현재의 좋은 습관을 계속 유지하세요.'
            })
        
        # 감정 균형 점수
        balance_score = self._calculate_emotional_balance(records[:30])
        
        return Response({
            'insights': insights,
            'patterns': patterns[:5],  # 상위 5개 패턴
            'recommendations': recommendations,
            'emotional_balance_score': balance_score,
            'analysis_period': {
                'start': records[min(99, len(records)-1)].created_at if records else None,
                'end': records[0].created_at if records else None,
                'record_count': len(records)
            }
        })
    
    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        """감정 기록에 노트 추가"""
        emotion_record = self.get_object()
        note = request.data.get('note', '')
        
        if not note:
            return Response(
                {'error': '노트 내용이 필요합니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        emotion_record.notes = (emotion_record.notes or '') + f'\n{timezone.now().isoformat()}: {note}'
        emotion_record.save()
        
        return Response(EmotionRecordSerializer(emotion_record).data)
    
    @action(detail=False, methods=['get'])
    def calendar(self, request):
        """캘린더 뷰를 위한 월별 감정 데이터"""
        year = int(request.query_params.get('year', timezone.now().year))
        month = int(request.query_params.get('month', timezone.now().month))
        
        records = self.get_queryset().filter(
            created_at__year=year,
            created_at__month=month
        )
        
        calendar_data = {}
        for record in records:
            date_key = record.created_at.date().isoformat()
            if date_key not in calendar_data:
                calendar_data[date_key] = {
                    'emotions': [],
                    'average_intensity': 0,
                    'count': 0
                }
            
            calendar_data[date_key]['emotions'].append({
                'type': record.emotion_type,
                'intensity': record.intensity,
                'time': record.created_at.time().isoformat()
            })
            calendar_data[date_key]['count'] += 1
        
        # 평균 계산
        for date_key in calendar_data:
            total_intensity = sum(e['intensity'] for e in calendar_data[date_key]['emotions'])
            calendar_data[date_key]['average_intensity'] = round(
                total_intensity / calendar_data[date_key]['count'], 2
            )
        
        return Response({
            'year': year,
            'month': month,
            'calendar': calendar_data
        })
    
    def _calculate_trend_direction(self, trends):
        """트렌드 방향 계산"""
        if len(trends) < 2:
            return 'stable'
        
        recent_avg = sum(t.get('average_intensity', 0) for t in trends[:3]) / 3
        past_avg = sum(t.get('average_intensity', 0) for t in trends[-3:]) / 3
        
        diff = recent_avg - past_avg
        if diff > 0.5:
            return 'improving'
        elif diff < -0.5:
            return 'declining'
        return 'stable'
    
    def _calculate_emotional_balance(self, records):
        """감정 균형 점수 계산 (0-100)"""
        if not records:
            return 50
        
        positive_emotions = ['happy', 'excited', 'grateful', 'peaceful', 'confident']
        negative_emotions = ['sad', 'angry', 'anxious', 'stressed', 'frustrated']
        
        positive_score = sum(
            r.intensity for r in records 
            if r.emotion_type in positive_emotions
        )
        negative_score = sum(
            r.intensity for r in records 
            if r.emotion_type in negative_emotions
        )
        
        total_score = positive_score + negative_score
        if total_score == 0:
            return 50
        
        balance = (positive_score / total_score) * 100
        return round(balance, 1)