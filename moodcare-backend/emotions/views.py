from rest_framework import generics, filters, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import Emotion, EmotionRecord
from .serializers import (
    EmotionSerializer,
    EmotionListSerializer,
    EmotionAnalysisRequestSerializer,
    EmotionStatisticsSerializer,
    EmotionInsightSerializer,
    EmotionTrendSerializer,
    VoiceAnalysisResponseSerializer
)
from .ai_analyzer import EmotionAnalyzer


class EmotionListCreateView(generics.ListCreateAPIView):
    """List and create emotions"""
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['emotion_type', 'intensity']
    search_fields = ['note', 'location', 'activity']
    ordering_fields = ['created_at', 'intensity']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Emotion.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EmotionListSerializer
        return EmotionSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmotionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, delete emotion"""
    permission_classes = (IsAuthenticated,)
    serializer_class = EmotionSerializer
    
    def get_queryset(self):
        return Emotion.objects.filter(user=self.request.user)


class EmotionStatsView(generics.GenericAPIView):
    """Get emotion statistics"""
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        emotions = Emotion.objects.filter(user=user)
        
        # Calculate statistics
        stats = {
            'total_records': emotions.count(),
            'emotion_distribution': {},
            'average_intensity': 0,
            'recent_mood': None
        }
        
        # Emotion distribution
        for emotion_type, label in Emotion.EMOTION_TYPES:
            count = emotions.filter(emotion_type=emotion_type).count()
            stats['emotion_distribution'][emotion_type] = count
        
        # Average intensity
        if emotions.exists():
            total_intensity = sum(e.intensity for e in emotions)
            stats['average_intensity'] = round(total_intensity / emotions.count(), 2)
            
            # Recent mood
            recent = emotions.first()
            if recent:
                stats['recent_mood'] = {
                    'emotion_type': recent.emotion_type,
                    'intensity': recent.intensity,
                    'created_at': recent.created_at
                }
        
        return Response(stats)