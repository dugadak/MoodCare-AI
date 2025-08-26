from django.urls import path
from .views import EmotionListCreateView, EmotionDetailView, EmotionStatsView

app_name = 'emotions'

urlpatterns = [
    path('', EmotionListCreateView.as_view(), name='emotion-list-create'),
    path('<int:pk>/', EmotionDetailView.as_view(), name='emotion-detail'),
    path('stats/', EmotionStatsView.as_view(), name='emotion-stats'),
]