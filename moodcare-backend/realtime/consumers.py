import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
import asyncio

class BaseConsumer(AsyncWebsocketConsumer):
    """Base WebSocket consumer with authentication"""
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.user = self.scope["user"]
        
        if self.user.is_anonymous:
            await self.close()
            return
            
        await self.channel_layer.group_add(
            f"user_{self.user.id}",
            self.channel_name
        )
        
        await self.accept()
        await self.send_json({
            "type": "connection",
            "message": "Connected successfully"
        })
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if hasattr(self, 'user') and not self.user.is_anonymous:
            await self.channel_layer.group_discard(
                f"user_{self.user.id}",
                self.channel_name
            )
    
    async def send_json(self, content):
        """Send JSON data to WebSocket"""
        await self.send(text_data=json.dumps(content))
    
    async def receive_json(self, content):
        """Receive and parse JSON data"""
        return json.loads(content)


class ChatConsumer(BaseConsumer):
    """실시간 채팅 Consumer"""
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await super().connect()
        
        # 입장 메시지 전송
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_join',
                'user': self.user.username,
                'timestamp': datetime.now().isoformat()
            }
        )
    
    async def disconnect(self, close_code):
        # 퇴장 메시지 전송
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_leave',
                'user': self.user.username,
                'timestamp': datetime.now().isoformat()
            }
        )
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        await super().disconnect(close_code)
    
    async def receive(self, text_data):
        """메시지 수신 및 브로드캐스트"""
        data = json.loads(text_data)
        message_type = data.get('type', 'message')
        
        if message_type == 'message':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data['message'],
                    'user': self.user.username,
                    'user_id': self.user.id,
                    'timestamp': datetime.now().isoformat()
                }
            )
        elif message_type == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_typing',
                    'user': self.user.username,
                    'is_typing': data.get('is_typing', False)
                }
            )
    
    async def chat_message(self, event):
        """채팅 메시지 전송"""
        await self.send_json({
            'type': 'message',
            'message': event['message'],
            'user': event['user'],
            'user_id': event['user_id'],
            'timestamp': event['timestamp']
        })
    
    async def chat_join(self, event):
        """사용자 입장 알림"""
        await self.send_json({
            'type': 'join',
            'user': event['user'],
            'message': f"{event['user']} joined the chat",
            'timestamp': event['timestamp']
        })
    
    async def chat_leave(self, event):
        """사용자 퇴장 알림"""
        await self.send_json({
            'type': 'leave',
            'user': event['user'],
            'message': f"{event['user']} left the chat",
            'timestamp': event['timestamp']
        })
    
    async def chat_typing(self, event):
        """타이핑 상태 전송"""
        await self.send_json({
            'type': 'typing',
            'user': event['user'],
            'is_typing': event['is_typing']
        })


class EmotionConsumer(BaseConsumer):
    """실시간 감정 공유 Consumer"""
    
    async def connect(self):
        await super().connect()
        
        # 감정 공유 그룹 참여
        self.emotion_group = 'emotion_sharing'
        await self.channel_layer.group_add(
            self.emotion_group,
            self.channel_name
        )
        
        # 현재 활성 사용자 수 전송
        await self.send_active_users_count()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.emotion_group,
            self.channel_name
        )
        await super().disconnect(close_code)
    
    async def receive(self, text_data):
        """감정 데이터 수신 및 브로드캐스트"""
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'share_emotion':
            # 감정 공유
            await self.channel_layer.group_send(
                self.emotion_group,
                {
                    'type': 'emotion_update',
                    'user': self.user.username,
                    'user_id': self.user.id,
                    'emotion': data.get('emotion'),
                    'intensity': data.get('intensity'),
                    'color': data.get('color'),
                    'message': data.get('message', ''),
                    'timestamp': datetime.now().isoformat()
                }
            )
        elif action == 'get_emotion_stats':
            # 실시간 감정 통계 요청
            stats = await self.get_emotion_statistics()
            await self.send_json({
                'type': 'emotion_stats',
                'stats': stats
            })
    
    async def emotion_update(self, event):
        """감정 업데이트 전송"""
        await self.send_json({
            'type': 'emotion_update',
            'user': event['user'],
            'user_id': event['user_id'],
            'emotion': event['emotion'],
            'intensity': event['intensity'],
            'color': event['color'],
            'message': event['message'],
            'timestamp': event['timestamp']
        })
    
    @database_sync_to_async
    def get_emotion_statistics(self):
        """실시간 감정 통계 조회"""
        from emotions.models import EmotionRecord
        from django.db.models import Count, Avg
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        last_hour = now - timedelta(hours=1)
        
        # 최근 1시간 감정 통계
        stats = EmotionRecord.objects.filter(
            created_at__gte=last_hour
        ).values('emotion_type').annotate(
            count=Count('id'),
            avg_intensity=Avg('intensity')
        )
        
        return list(stats)
    
    async def send_active_users_count(self):
        """활성 사용자 수 전송"""
        # 실제로는 Redis나 캐시에서 활성 사용자 수를 가져와야 함
        active_users = 1  # Placeholder
        await self.send_json({
            'type': 'active_users',
            'count': active_users
        })


class MusicConsumer(BaseConsumer):
    """실시간 음악 공유 Consumer"""
    
    async def connect(self):
        await super().connect()
        
        # 음악 공유 그룹 참여
        self.music_group = 'music_sharing'
        await self.channel_layer.group_add(
            self.music_group,
            self.channel_name
        )
        
        # 현재 재생 중인 음악 목록 전송
        await self.send_now_playing()
    
    async def disconnect(self, close_code):
        # 음악 재생 중단 알림
        await self.channel_layer.group_send(
            self.music_group,
            {
                'type': 'music_stopped',
                'user': self.user.username,
                'user_id': self.user.id
            }
        )
        
        await self.channel_layer.group_discard(
            self.music_group,
            self.channel_name
        )
        await super().disconnect(close_code)
    
    async def receive(self, text_data):
        """음악 재생 정보 수신"""
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'now_playing':
            # 현재 재생 중인 음악 공유
            await self.channel_layer.group_send(
                self.music_group,
                {
                    'type': 'music_playing',
                    'user': self.user.username,
                    'user_id': self.user.id,
                    'track': data.get('track'),
                    'artist': data.get('artist'),
                    'album': data.get('album'),
                    'emotion': data.get('emotion'),
                    'timestamp': datetime.now().isoformat()
                }
            )
        elif action == 'like_track':
            # 음악 좋아요
            await self.channel_layer.group_send(
                self.music_group,
                {
                    'type': 'track_liked',
                    'user': self.user.username,
                    'track': data.get('track'),
                    'artist': data.get('artist')
                }
            )
        elif action == 'create_playlist':
            # 플레이리스트 생성 알림
            await self.channel_layer.group_send(
                self.music_group,
                {
                    'type': 'playlist_created',
                    'user': self.user.username,
                    'playlist_name': data.get('playlist_name'),
                    'emotion': data.get('emotion')
                }
            )
    
    async def music_playing(self, event):
        """재생 중인 음악 정보 전송"""
        await self.send_json({
            'type': 'now_playing',
            'user': event['user'],
            'user_id': event['user_id'],
            'track': event['track'],
            'artist': event['artist'],
            'album': event['album'],
            'emotion': event['emotion'],
            'timestamp': event['timestamp']
        })
    
    async def music_stopped(self, event):
        """음악 중단 알림"""
        await self.send_json({
            'type': 'stopped',
            'user': event['user'],
            'user_id': event['user_id']
        })
    
    async def track_liked(self, event):
        """트랙 좋아요 알림"""
        await self.send_json({
            'type': 'track_liked',
            'user': event['user'],
            'track': event['track'],
            'artist': event['artist']
        })
    
    async def playlist_created(self, event):
        """플레이리스트 생성 알림"""
        await self.send_json({
            'type': 'playlist_created',
            'user': event['user'],
            'playlist_name': event['playlist_name'],
            'emotion': event['emotion']
        })
    
    async def send_now_playing(self):
        """현재 재생 중인 음악 목록 전송"""
        # 실제로는 캐시나 DB에서 가져와야 함
        now_playing = []  # Placeholder
        await self.send_json({
            'type': 'now_playing_list',
            'tracks': now_playing
        })


class NotificationConsumer(BaseConsumer):
    """실시간 알림 Consumer"""
    
    async def connect(self):
        await super().connect()
        
        # 개인 알림 채널
        self.user_group = f'notifications_{self.user.id}'
        await self.channel_layer.group_add(
            self.user_group,
            self.channel_name
        )
        
        # 읽지 않은 알림 전송
        await self.send_unread_notifications()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group,
            self.channel_name
        )
        await super().disconnect(close_code)
    
    async def receive(self, text_data):
        """알림 관련 액션 처리"""
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'mark_read':
            notification_id = data.get('notification_id')
            await self.mark_notification_read(notification_id)
        elif action == 'mark_all_read':
            await self.mark_all_notifications_read()
    
    async def send_notification(self, event):
        """알림 전송"""
        await self.send_json({
            'type': 'notification',
            'id': event.get('id'),
            'title': event.get('title'),
            'message': event.get('message'),
            'category': event.get('category'),
            'priority': event.get('priority', 'normal'),
            'data': event.get('data', {}),
            'timestamp': event.get('timestamp', datetime.now().isoformat())
        })
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """알림 읽음 처리"""
        # 실제 구현 필요
        pass
    
    @database_sync_to_async
    def mark_all_notifications_read(self):
        """모든 알림 읽음 처리"""
        # 실제 구현 필요
        pass
    
    async def send_unread_notifications(self):
        """읽지 않은 알림 전송"""
        # 실제로는 DB에서 가져와야 함
        unread = []  # Placeholder
        await self.send_json({
            'type': 'unread_notifications',
            'notifications': unread,
            'count': len(unread)
        })
    
    # 다양한 알림 타입 핸들러
    async def emotion_reminder(self, event):
        """감정 기록 리마인더"""
        await self.send_json({
            'type': 'reminder',
            'category': 'emotion',
            'title': '감정 기록 시간',
            'message': event.get('message', '오늘의 감정을 기록해보세요'),
            'timestamp': datetime.now().isoformat()
        })
    
    async def story_complete(self, event):
        """스토리 완료 알림"""
        await self.send_json({
            'type': 'achievement',
            'category': 'story',
            'title': '스토리 완료',
            'message': event.get('message'),
            'story_id': event.get('story_id'),
            'timestamp': datetime.now().isoformat()
        })
    
    async def music_recommendation(self, event):
        """음악 추천 알림"""
        await self.send_json({
            'type': 'recommendation',
            'category': 'music',
            'title': '새로운 음악 추천',
            'message': event.get('message'),
            'tracks': event.get('tracks', []),
            'timestamp': datetime.now().isoformat()
        })