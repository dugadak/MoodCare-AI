from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoryViewSet, StoryTemplateViewSet

# Create routers
router = DefaultRouter()
router.register(r'stories', StoryViewSet, basename='story')
router.register(r'templates', StoryTemplateViewSet, basename='story-template')

app_name = 'stories'

urlpatterns = [
    path('', include(router.urls)),
    
    # Custom story endpoints handled by ViewSet:
    # /stories/generate/ - Generate new story
    # /stories/{id}/continue/ - Continue interactive story
    # /stories/{id}/interact/ - Record interaction
    # /stories/{id}/complete/ - Mark as completed
    # /stories/library/ - User's story library
    # /templates/ - Story templates
]