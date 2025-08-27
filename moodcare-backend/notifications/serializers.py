from rest_framework import serializers
from .models import DeviceToken, NotificationTemplate, NotificationLog, NotificationPreference


class DeviceTokenSerializer(serializers.ModelSerializer):
    """FCM 디바이스 토큰 시리얼라이저"""
    
    class Meta:
        model = DeviceToken
        fields = ['id', 'token', 'device_type', 'device_id', 'is_active', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """토큰 생성 또는 업데이트"""
        user = self.context['request'].user
        device_id = validated_data.get('device_id', validated_data['token'][:50])
        
        token, created = DeviceToken.objects.update_or_create(
            user=user,
            device_id=device_id,
            defaults={
                'token': validated_data['token'],
                'device_type': validated_data['device_type'],
                'is_active': True,
            }
        )
        
        return token


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """알림 설정 시리얼라이저"""
    
    class Meta:
        model = NotificationPreference
        fields = [
            'emotion_reminder', 'story_updates', 'music_recommendations',
            'achievements', 'system_notifications',
            'daily_reminder_enabled', 'daily_reminder_time',
            'weekly_summary_enabled', 'weekly_summary_day',
            'quiet_hours_enabled', 'quiet_hours_start', 'quiet_hours_end',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def update(self, instance, validated_data):
        """알림 설정 업데이트"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class NotificationLogSerializer(serializers.ModelSerializer):
    """알림 로그 시리얼라이저"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = NotificationLog
        fields = [
            'id', 'template_name', 'title', 'body', 'data', 
            'category', 'status', 'sent_at', 'read_at', 
            'error_message', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """알림 템플릿 시리얼라이저"""
    
    class Meta:
        model = NotificationTemplate
        fields = [
            'id', 'name', 'title', 'body', 'data_template',
            'category', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SendNotificationSerializer(serializers.Serializer):
    """알림 발송 시리얼라이저"""
    title = serializers.CharField(max_length=255)
    body = serializers.CharField()
    data = serializers.JSONField(required=False, default=dict)
    category = serializers.ChoiceField(
        choices=['emotion_reminder', 'story_update', 'music_recommendation', 
                 'achievement', 'system'],
        default='general'
    )
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    
    def validate_user_ids(self, value):
        """사용자 ID 검증"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if value:
            existing_ids = User.objects.filter(id__in=value).values_list('id', flat=True)
            invalid_ids = set(value) - set(existing_ids)
            if invalid_ids:
                raise serializers.ValidationError(f"Invalid user IDs: {invalid_ids}")
        return value


class TestNotificationSerializer(serializers.Serializer):
    """테스트 알림 시리얼라이저"""
    type = serializers.ChoiceField(
        choices=['emotion_reminder', 'story_complete', 'music_recommendation', 'achievement'],
        default='emotion_reminder'
    )
    custom_title = serializers.CharField(required=False, allow_blank=True)
    custom_body = serializers.CharField(required=False, allow_blank=True)