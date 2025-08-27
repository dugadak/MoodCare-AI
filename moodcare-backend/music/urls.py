from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MusicRecommendationViewSet,
    MusicProfileViewSet,
    MusicDiaryViewSet,
    TherapeuticSoundViewSet
)

# Create routers
router = DefaultRouter()
router.register(r'recommendations', MusicRecommendationViewSet, basename='music-recommendation')
router.register(r'profile', MusicProfileViewSet, basename='music-profile')
router.register(r'diary', MusicDiaryViewSet, basename='music-diary')
router.register(r'therapeutic', TherapeuticSoundViewSet, basename='therapeutic-sound')

app_name = 'music'

urlpatterns = [
    path('', include(router.urls)),
    
    # Custom music endpoints handled by ViewSets:
    # /recommendations/generate/ - Get AI recommendations
    # /recommendations/feedback/ - Submit feedback
    # /profile/update-preferences/ - Update music preferences
    # /diary/today/ - Today's music diary
    # /diary/analytics/ - Music listening analytics
    # /therapeutic/categories/ - Get therapeutic categories
    # /therapeutic/binaural/ - Binaural beats
]