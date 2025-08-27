from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DeviceToken(models.Model):
    """FCM 디바이스 토큰 관리"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_tokens')
    token = models.TextField(unique=True)
    device_type = models.CharField(max_length=20, choices=[
        ('ios', 'iOS'),
        ('android', 'Android'),
        ('web', 'Web'),
    ])
    device_id = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'device_id']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.device_type}"


class NotificationTemplate(models.Model):
    """알림 템플릿"""
    name = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    data_template = models.JSONField(default=dict, blank=True)
    category = models.CharField(max_length=50, choices=[
        ('emotion_reminder', '감정 리마인더'),
        ('story_update', '스토리 업데이트'),
        ('music_recommendation', '음악 추천'),
        ('achievement', '업적'),
        ('system', '시스템'),
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class NotificationLog(models.Model):
    """알림 발송 로그"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_logs')
    template = models.ForeignKey(NotificationTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    category = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[
        ('pending', '대기'),
        ('sent', '발송'),
        ('failed', '실패'),
        ('read', '읽음'),
    ], default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class NotificationPreference(models.Model):
    """사용자 알림 설정"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preference')
    
    # 알림 유형별 설정
    emotion_reminder = models.BooleanField(default=True)
    story_updates = models.BooleanField(default=True)
    music_recommendations = models.BooleanField(default=True)
    achievements = models.BooleanField(default=True)
    system_notifications = models.BooleanField(default=True)
    
    # 리마인더 설정
    daily_reminder_enabled = models.BooleanField(default=False)
    daily_reminder_time = models.TimeField(null=True, blank=True)
    weekly_summary_enabled = models.BooleanField(default=False)
    weekly_summary_day = models.IntegerField(default=1, choices=[
        (0, '월요일'),
        (1, '화요일'),
        (2, '수요일'),
        (3, '목요일'),
        (4, '금요일'),
        (5, '토요일'),
        (6, '일요일'),
    ])
    
    # 방해 금지 모드
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - Preferences"