import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
from django.utils import timezone
from typing import List, Dict, Optional
import logging
from .models import DeviceToken, NotificationLog, NotificationPreference

logger = logging.getLogger(__name__)

class FCMService:
    """Firebase Cloud Messaging 서비스"""
    
    _initialized = False
    
    @classmethod
    def initialize(cls):
        """Firebase Admin SDK 초기화"""
        if cls._initialized:
            return
        
        try:
            # Firebase 자격 증명 파일 경로
            cred_path = settings.BASE_DIR / 'firebase-credentials.json'
            
            if cred_path.exists():
                cred = credentials.Certificate(str(cred_path))
                firebase_admin.initialize_app(cred)
                cls._initialized = True
                logger.info("Firebase Admin SDK initialized successfully")
            else:
                logger.warning(f"Firebase credentials file not found at {cred_path}")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase Admin SDK: {e}")
    
    @classmethod
    def send_to_user(cls, user, title: str, body: str, 
                     data: Optional[Dict] = None, 
                     category: str = 'general') -> bool:
        """특정 사용자에게 알림 발송"""
        cls.initialize()
        
        # 사용자 알림 설정 확인
        if not cls._check_user_preferences(user, category):
            logger.info(f"User {user.username} has disabled {category} notifications")
            return False
        
        # 활성 토큰 가져오기
        tokens = DeviceToken.objects.filter(
            user=user,
            is_active=True
        ).values_list('token', flat=True)
        
        if not tokens:
            logger.warning(f"No active tokens found for user {user.username}")
            return False
        
        # 알림 로그 생성
        notification_log = NotificationLog.objects.create(
            user=user,
            title=title,
            body=body,
            data=data or {},
            category=category,
            status='pending'
        )
        
        try:
            # FCM 메시지 생성
            message = messaging.MulticastMessage(
                tokens=list(tokens),
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data={
                    'category': category,
                    'notification_id': str(notification_log.id),
                    **(data or {})
                },
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        channel_id=cls._get_channel_id(category),
                        click_action='FLUTTER_NOTIFICATION_CLICK',
                    ),
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            badge=1,
                            sound='default',
                        ),
                    ),
                ),
            )
            
            # 메시지 발송
            response = messaging.send_multicast(message)
            
            # 성공한 토큰 처리
            if response.success_count > 0:
                notification_log.status = 'sent'
                notification_log.sent_at = timezone.now()
                notification_log.save()
                logger.info(f"Successfully sent notification to {response.success_count} devices")
            
            # 실패한 토큰 처리
            if response.failure_count > 0:
                failed_tokens = [
                    tokens[idx] for idx, resp in enumerate(response.responses)
                    if not resp.success
                ]
                cls._handle_failed_tokens(failed_tokens)
            
            return response.success_count > 0
            
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            notification_log.status = 'failed'
            notification_log.error_message = str(e)
            notification_log.save()
            return False
    
    @classmethod
    def send_to_users(cls, users, title: str, body: str,
                      data: Optional[Dict] = None,
                      category: str = 'general') -> int:
        """여러 사용자에게 알림 발송"""
        success_count = 0
        
        for user in users:
            if cls.send_to_user(user, title, body, data, category):
                success_count += 1
        
        return success_count
    
    @classmethod
    def send_emotion_reminder(cls, user):
        """감정 기록 리마인더 발송"""
        title = "감정 기록 시간 🌟"
        body = "오늘 하루는 어떠셨나요? 지금 감정을 기록해보세요."
        data = {
            'type': 'emotion_reminder',
            'action': 'open_emotion_input'
        }
        
        return cls.send_to_user(user, title, body, data, 'emotion_reminder')
    
    @classmethod
    def send_story_complete(cls, user, story_title: str):
        """스토리 완료 알림"""
        title = "스토리 완료 📚"
        body = f"'{story_title}' 스토리를 완료했습니다!"
        data = {
            'type': 'story_complete',
            'action': 'open_story_list'
        }
        
        return cls.send_to_user(user, title, body, data, 'story_update')
    
    @classmethod
    def send_music_recommendation(cls, user, track_count: int):
        """음악 추천 알림"""
        title = "새로운 음악 추천 🎵"
        body = f"당신의 감정에 맞는 {track_count}개의 음악을 준비했어요."
        data = {
            'type': 'music_recommendation',
            'action': 'open_music_list'
        }
        
        return cls.send_to_user(user, title, body, data, 'music_recommendation')
    
    @classmethod
    def send_achievement(cls, user, achievement: str):
        """업적 달성 알림"""
        title = "업적 달성! 🏆"
        body = f"{achievement} 업적을 달성했습니다!"
        data = {
            'type': 'achievement',
            'achievement': achievement
        }
        
        return cls.send_to_user(user, title, body, data, 'achievement')
    
    @classmethod
    def register_token(cls, user, token: str, device_type: str,
                      device_id: Optional[str] = None):
        """FCM 토큰 등록"""
        try:
            device_token, created = DeviceToken.objects.update_or_create(
                user=user,
                device_id=device_id or token[:50],  # device_id가 없으면 토큰 일부 사용
                defaults={
                    'token': token,
                    'device_type': device_type,
                    'is_active': True,
                }
            )
            
            if created:
                logger.info(f"New device token registered for user {user.username}")
            else:
                logger.info(f"Device token updated for user {user.username}")
            
            return device_token
            
        except Exception as e:
            logger.error(f"Failed to register token: {e}")
            return None
    
    @classmethod
    def deactivate_token(cls, token: str):
        """토큰 비활성화"""
        try:
            DeviceToken.objects.filter(token=token).update(is_active=False)
            logger.info(f"Token deactivated: {token[:20]}...")
        except Exception as e:
            logger.error(f"Failed to deactivate token: {e}")
    
    @classmethod
    def _check_user_preferences(cls, user, category: str) -> bool:
        """사용자 알림 설정 확인"""
        try:
            pref = NotificationPreference.objects.get(user=user)
            
            # 방해 금지 모드 확인
            if pref.quiet_hours_enabled:
                now = timezone.now().time()
                if pref.quiet_hours_start <= now <= pref.quiet_hours_end:
                    return False
            
            # 카테고리별 설정 확인
            category_map = {
                'emotion_reminder': pref.emotion_reminder,
                'story_update': pref.story_updates,
                'music_recommendation': pref.music_recommendations,
                'achievement': pref.achievements,
                'system': pref.system_notifications,
            }
            
            return category_map.get(category, True)
            
        except NotificationPreference.DoesNotExist:
            # 설정이 없으면 기본값으로 허용
            return True
    
    @classmethod
    def _get_channel_id(cls, category: str) -> str:
        """Android 알림 채널 ID 반환"""
        channel_map = {
            'emotion_reminder': 'emotion_reminder',
            'story_update': 'story',
            'music_recommendation': 'music',
            'achievement': 'general',
            'system': 'general',
        }
        return channel_map.get(category, 'general')
    
    @classmethod
    def _handle_failed_tokens(cls, tokens: List[str]):
        """실패한 토큰 처리"""
        for token in tokens:
            cls.deactivate_token(token)