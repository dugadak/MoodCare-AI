"""
URL configuration for moodcare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """MoodCare AI API Root"""
    return Response({
        'message': 'MoodCare AI - Emotional Wellness Platform API',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'register': '/api/v1/auth/register/',
                'login': '/api/v1/auth/login/',
                'logout': '/api/v1/auth/logout/',
                'refresh': '/api/v1/auth/refresh/',
                'profile': '/api/v1/auth/profile/'
            },
            'emotions': {
                'records': '/api/v1/emotions/records/',
                'analyze_text': '/api/v1/emotions/records/analyze/text/',
                'analyze_voice': '/api/v1/emotions/records/analyze/voice/',
                'statistics': '/api/v1/emotions/records/statistics/',
                'trends': '/api/v1/emotions/records/trends/',
                'insights': '/api/v1/emotions/records/insights/'
            },
            'stories': {
                'list': '/api/v1/stories/stories/',
                'generate': '/api/v1/stories/stories/generate/',
                'templates': '/api/v1/stories/templates/'
            },
            'music': {
                'recommendations': '/api/v1/music/recommendations/',
                'profile': '/api/v1/music/profile/',
                'diary': '/api/v1/music/diary/',
                'therapeutic': '/api/v1/music/therapeutic/'
            }
        },
        'documentation': '/api/docs/',
        'websocket': 'ws://localhost:8000/ws/'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    
    # API v1 endpoints
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/emotions/', include('emotions.urls')),
    path('api/v1/stories/', include('stories.urls')),
    path('api/v1/music/', include('music.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    
    # Legacy endpoints (for backward compatibility)
    path('api/users/', include('users.urls')),
    path('api/emotions/', include('emotions.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
