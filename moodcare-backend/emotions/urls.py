from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmotionListCreateView, 
    EmotionDetailView, 
    EmotionStatsView,
    EmotionViewSet
)

# Create router for ViewSet
router = DefaultRouter()
router.register(r'records', EmotionViewSet, basename='emotion-record')

app_name = 'emotions'

urlpatterns = [
    # ViewSet routes with custom actions
    path('', include(router.urls)),
    
    # Legacy/simple endpoints
    path('list/', EmotionListCreateView.as_view(), name='emotion-list-create'),
    path('detail/<int:pk>/', EmotionDetailView.as_view(), name='emotion-detail'),
    path('stats/', EmotionStatsView.as_view(), name='emotion-stats'),
    
    # Custom emotion analysis endpoints (handled by ViewSet)
    # /records/analyze/text/
    # /records/analyze/voice/
    # /records/statistics/
    # /records/trends/
    # /records/insights/
]