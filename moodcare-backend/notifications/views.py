from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import DeviceToken, NotificationTemplate, NotificationLog, NotificationPreference
from .serializers import (
    DeviceTokenSerializer,
    NotificationPreferenceSerializer,
    NotificationLogSerializer,
    NotificationTemplateSerializer,
    SendNotificationSerializer,
    TestNotificationSerializer
)
from .fcm_service import FCMService

User = get_user_model()


class DeviceTokenViewSet(viewsets.ModelViewSet):
    """FCM 디바이스 토큰 관리"""
    serializer_class = DeviceTokenSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """사용자의 토큰만 반환"""
        return DeviceToken.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """FCM 토큰 등록"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # FCM 서비스에 토큰 등록
        token_obj = FCMService.register_token(
            user=request.user,
            token=serializer.validated_data['token'],
            device_type=serializer.validated_data['device_type'],
            device_id=serializer.validated_data.get('device_id')
        )
        
        if token_obj:
            return Response(
                DeviceTokenSerializer(token_obj).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': 'Failed to register token'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    def deactivate(self, request):
        """토큰 비활성화"""
        token = request.data.get('token')
        if not token:
            return Response(
                {'error': 'Token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        FCMService.deactivate_token(token)
        return Response({'status': 'Token deactivated'})


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """알림 설정 관리"""
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch']
    
    def get_queryset(self):
        """사용자의 알림 설정만 반환"""
        return NotificationPreference.objects.filter(user=self.request.user)
    
    def get_object(self):
        """사용자의 알림 설정 가져오기 (없으면 생성)"""
        obj, created = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return obj
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """현재 사용자의 알림 설정"""
        preference = self.get_object()
        serializer = self.get_serializer(preference)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def toggle_category(self, request):
        """특정 카테고리 알림 토글"""
        category = request.data.get('category')
        category_map = {
            'emotion_reminder': 'emotion_reminder',
            'story_update': 'story_updates',
            'music_recommendation': 'music_recommendations',
            'achievement': 'achievements',
            'system': 'system_notifications',
        }
        
        if category not in category_map:
            return Response(
                {'error': 'Invalid category'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        preference = self.get_object()
        field_name = category_map[category]
        current_value = getattr(preference, field_name)
        setattr(preference, field_name, not current_value)
        preference.save()
        
        return Response({
            'category': category,
            'enabled': not current_value
        })


class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """알림 로그 조회"""
    serializer_class = NotificationLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """사용자의 알림 로그만 반환"""
        queryset = NotificationLog.objects.filter(user=self.request.user)
        
        # 필터링
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # 읽지 않은 알림만
        unread_only = self.request.query_params.get('unread', '').lower() == 'true'
        if unread_only:
            queryset = queryset.filter(status='sent', read_at__isnull=True)
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """알림을 읽음으로 표시"""
        try:
            notification = self.get_object()
            notification.status = 'read'
            notification.read_at = timezone.now()
            notification.save()
            
            return Response({'status': 'marked as read'})
        except NotificationLog.DoesNotExist:
            return Response(
                {'error': 'Notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """모든 알림을 읽음으로 표시"""
        updated_count = NotificationLog.objects.filter(
            user=request.user,
            status='sent',
            read_at__isnull=True
        ).update(
            status='read',
            read_at=timezone.now()
        )
        
        return Response({
            'status': 'marked all as read',
            'count': updated_count
        })


class NotificationViewSet(viewsets.ViewSet):
    """알림 발송 관리"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def send(self, request):
        """알림 발송"""
        serializer = SendNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        user_ids = data.get('user_ids', [request.user.id])
        users = User.objects.filter(id__in=user_ids)
        
        # 알림 발송
        success_count = FCMService.send_to_users(
            users=users,
            title=data['title'],
            body=data['body'],
            data=data.get('data', {}),
            category=data['category']
        )
        
        return Response({
            'status': 'sent',
            'success_count': success_count,
            'total_users': len(users)
        })
    
    @action(detail=False, methods=['post'])
    def send_test(self, request):
        """테스트 알림 발송"""
        serializer = TestNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        notification_type = serializer.validated_data['type']
        custom_title = serializer.validated_data.get('custom_title', '')
        custom_body = serializer.validated_data.get('custom_body', '')
        
        # 알림 타입별 발송
        success = False
        if notification_type == 'emotion_reminder':
            success = FCMService.send_emotion_reminder(request.user)
        elif notification_type == 'story_complete':
            title = custom_title or '테스트 스토리'
            success = FCMService.send_story_complete(request.user, title)
        elif notification_type == 'music_recommendation':
            track_count = 5
            success = FCMService.send_music_recommendation(request.user, track_count)
        elif notification_type == 'achievement':
            achievement = custom_title or '첫 감정 기록'
            success = FCMService.send_achievement(request.user, achievement)
        
        if success:
            return Response({'status': 'Test notification sent'})
        else:
            return Response(
                {'error': 'Failed to send test notification'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """알림 통계"""
        logs = NotificationLog.objects.filter(user=request.user)
        
        # 카테고리별 통계
        category_stats = {}
        for category in ['emotion_reminder', 'story_update', 'music_recommendation', 'achievement', 'system']:
            category_logs = logs.filter(category=category)
            category_stats[category] = {
                'total': category_logs.count(),
                'sent': category_logs.filter(status='sent').count(),
                'read': category_logs.filter(status='read').count(),
                'failed': category_logs.filter(status='failed').count(),
            }
        
        # 전체 통계
        total_stats = {
            'total': logs.count(),
            'sent': logs.filter(status='sent').count(),
            'read': logs.filter(status='read').count(),
            'failed': logs.filter(status='failed').count(),
            'unread': logs.filter(status='sent', read_at__isnull=True).count(),
        }
        
        # 활성 토큰 수
        active_tokens = DeviceToken.objects.filter(
            user=request.user,
            is_active=True
        ).count()
        
        return Response({
            'total': total_stats,
            'by_category': category_stats,
            'active_tokens': active_tokens,
        })