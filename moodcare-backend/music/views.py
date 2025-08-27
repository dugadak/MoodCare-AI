from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Avg, Count, Sum, Q
from datetime import datetime, timedelta
import json

from .models import (
    MusicProfile, MusicRecommendation, MusicDiary,
    AudioVisualization, TherapeuticSound
)
from .serializers import (
    MusicProfileSerializer,
    MusicRecommendationSerializer,
    MusicRecommendationRequestSerializer,
    MusicDiarySerializer,
    AudioVisualizationSerializer,
    TherapeuticSoundSerializer,
    PlaylistGenerationRequestSerializer,
    MusicFeedbackSerializer,
    MusicAnalyticsSerializer
)
from .recommender import MusicRecommender


class MusicRecommendationViewSet(viewsets.ModelViewSet):
    """ViewSet for music recommendations"""
    serializer_class = MusicRecommendationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter recommendations by user"""
        queryset = MusicRecommendation.objects.filter(user=self.request.user)
        
        # Filter by recommendation type if provided
        rec_type = self.request.query_params.get('type')
        if rec_type:
            queryset = queryset.filter(recommendation_type=rec_type)
        
        # Filter by date range
        days = self.request.query_params.get('days', 7)
        start_date = timezone.now() - timedelta(days=int(days))
        queryset = queryset.filter(created_at__gte=start_date)
        
        return queryset.order_by('-created_at')
    
    @action(detail=False, methods=['post'], url_path='generate')
    def generate(self, request):
        """Generate AI-powered music recommendations"""
        serializer = MusicRecommendationRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Initialize recommender
            recommender = MusicRecommender()
            
            # Get recommendations
            recommendations = recommender.get_recommendations(
                current_emotion=data['current_emotion'],
                emotion_intensity=data['emotion_intensity'],
                target_emotion=data.get('target_emotion'),
                recommendation_type=data.get('recommendation_type', 'mood_boost'),
                preferences={
                    'genres': data.get('genre_preference', []),
                    'energy_level': data.get('energy_level'),
                    'context': data.get('context')
                }
            )
            
            # Save recommendations to database
            saved_recommendations = []
            for rec in recommendations:
                music_rec = MusicRecommendation.objects.create(
                    user=request.user,
                    target_emotion=data.get('target_emotion', data['current_emotion']),
                    recommendation_type=data.get('recommendation_type', 'mood_boost'),
                    track_id=rec['track_id'],
                    track_name=rec['track_name'],
                    artist=rec['artist'],
                    album=rec.get('album', ''),
                    audio_features=rec.get('audio_features', {}),
                    recommendation_score=rec.get('recommendation_score', 0.5),
                    recommendation_reason=rec.get('recommendation_reason', '')
                )
                saved_recommendations.append(music_rec)
            
            # Serialize and return
            response_serializer = MusicRecommendationSerializer(
                saved_recommendations, many=True
            )
            
            return Response({
                'recommendations': response_serializer.data,
                'count': len(saved_recommendations),
                'generation_time': timezone.now()
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='feedback')
    def feedback(self, request, pk=None):
        """Submit feedback for a music recommendation"""
        recommendation = self.get_object()
        serializer = MusicFeedbackSerializer(data=request.data)
        
        if serializer.is_valid():
            # Update recommendation with feedback
            recommendation.user_rating = serializer.validated_data.get('rating')
            recommendation.helped_mood = serializer.validated_data.get('helped_mood')
            recommendation.skipped = serializer.validated_data.get('skipped', False)
            
            if not recommendation.skipped:
                recommendation.play_count += 1
                recommendation.played_at = timezone.now()
            
            recommendation.save()
            
            # Update user's music profile
            profile, created = MusicProfile.objects.get_or_create(
                user=request.user
            )
            
            # Update emotion-music mapping based on feedback
            if recommendation.helped_mood:
                emotion = recommendation.target_emotion
                if emotion not in profile.music_for_emotions:
                    profile.music_for_emotions[emotion] = []
                profile.music_for_emotions[emotion].append(recommendation.track_id)
                
                # Add to healing playlist if it helped
                if recommendation.track_id not in profile.healing_playlist:
                    profile.healing_playlist.append(recommendation.track_id)
            elif recommendation.skipped:
                # Add to trigger songs if skipped
                if recommendation.track_id not in profile.trigger_songs:
                    profile.trigger_songs.append(recommendation.track_id)
            
            profile.save()
            
            return Response({
                'message': 'Feedback recorded successfully',
                'recommendation_id': recommendation.id
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='playlist')
    def playlist(self, request):
        """Get a curated playlist based on current mood"""
        emotion = request.query_params.get('emotion', 'neutral')
        duration = int(request.query_params.get('duration', 30))  # minutes
        
        # Get recent successful recommendations
        recommendations = MusicRecommendation.objects.filter(
            user=request.user,
            target_emotion=emotion,
            helped_mood=True
        ).order_by('-recommendation_score')[:duration // 3]  # ~3 min per song
        
        if not recommendations:
            # Generate new recommendations if none exist
            return self.generate(request)
        
        serializer = MusicRecommendationSerializer(recommendations, many=True)
        
        return Response({
            'playlist': serializer.data,
            'total_duration': len(recommendations) * 3,  # approximate
            'emotion': emotion
        }, status=status.HTTP_200_OK)


class MusicProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user music profiles"""
    serializer_class = MusicProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get user's music profile"""
        return MusicProfile.objects.filter(user=self.request.user)
    
    def get_object(self):
        """Get or create user's music profile"""
        profile, created = MusicProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile
    
    @action(detail=False, methods=['post'], url_path='update-preferences')
    def update_preferences(self, request):
        """Update music preferences"""
        profile = self.get_object()
        
        # Update preferences
        if 'genres' in request.data:
            profile.preferred_genres = request.data['genres']
        if 'artists' in request.data:
            profile.preferred_artists = request.data['artists']
        if 'energy_level' in request.data:
            profile.preferred_energy_level = request.data['energy_level']
        if 'tempo' in request.data:
            profile.preferred_tempo = request.data['tempo']
        
        profile.save()
        
        serializer = MusicProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='listening-patterns')
    def listening_patterns(self, request):
        """Get user's listening patterns"""
        profile = self.get_object()
        
        # Analyze listening history
        recommendations = MusicRecommendation.objects.filter(
            user=request.user,
            play_count__gt=0
        )
        
        # Calculate patterns
        patterns = {
            'most_played_emotion': '',
            'preferred_time': [],
            'average_energy': 0,
            'total_listening_time': 0,
            'favorite_recommendation_type': ''
        }
        
        if recommendations.exists():
            # Most played emotion
            emotion_counts = recommendations.values('target_emotion').annotate(
                count=Count('id')
            ).order_by('-count')
            if emotion_counts:
                patterns['most_played_emotion'] = emotion_counts[0]['target_emotion']
            
            # Average energy level
            energy_sum = 0
            energy_count = 0
            for rec in recommendations:
                if rec.audio_features and 'energy' in rec.audio_features:
                    energy_sum += rec.audio_features['energy']
                    energy_count += 1
            if energy_count > 0:
                patterns['average_energy'] = round(energy_sum / energy_count, 2)
            
            # Total listening time (approximate)
            patterns['total_listening_time'] = recommendations.aggregate(
                total=Sum('play_count')
            )['total'] * 3  # ~3 minutes per song
            
            # Favorite recommendation type
            type_counts = recommendations.values('recommendation_type').annotate(
                count=Count('id')
            ).order_by('-count')
            if type_counts:
                patterns['favorite_recommendation_type'] = type_counts[0]['recommendation_type']
        
        return Response(patterns, status=status.HTTP_200_OK)


class MusicDiaryViewSet(viewsets.ModelViewSet):
    """ViewSet for music diary entries"""
    serializer_class = MusicDiarySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get user's music diary entries"""
        return MusicDiary.objects.filter(user=self.request.user).order_by('-date')
    
    @action(detail=False, methods=['get'], url_path='today')
    def today(self, request):
        """Get or create today's music diary"""
        today = timezone.now().date()
        diary, created = MusicDiary.objects.get_or_create(
            user=request.user,
            date=today,
            defaults={
                'dominant_emotion': 'neutral',
                'energy_level': 0.5
            }
        )
        
        serializer = MusicDiarySerializer(diary)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='analytics')
    def analytics(self, request):
        """Get music listening analytics"""
        period = request.query_params.get('period', '30days')
        
        # Determine date range
        if period == '7days':
            start_date = timezone.now() - timedelta(days=7)
        elif period == '30days':
            start_date = timezone.now() - timedelta(days=30)
        else:
            start_date = timezone.now() - timedelta(days=90)
        
        # Get diary entries in period
        diaries = self.get_queryset().filter(date__gte=start_date)
        
        # Get recommendations in period
        recommendations = MusicRecommendation.objects.filter(
            user=request.user,
            created_at__gte=start_date
        )
        
        # Calculate analytics
        analytics_data = {
            'period': period,
            'total_listening_time': 0,
            'favorite_genre': 'unknown',
            'favorite_artist': 'unknown',
            'mood_improvement_rate': 0,
            'most_effective_type': 'unknown',
            'emotion_music_correlation': {},
            'listening_patterns': {},
            'therapeutic_effectiveness': 0
        }
        
        if recommendations.exists():
            # Total listening time
            analytics_data['total_listening_time'] = recommendations.aggregate(
                total=Sum('play_count')
            )['total'] * 3  # ~3 minutes per song
            
            # Mood improvement rate
            helped_count = recommendations.filter(helped_mood=True).count()
            total_count = recommendations.count()
            analytics_data['mood_improvement_rate'] = round(
                (helped_count / total_count) * 100, 2
            ) if total_count > 0 else 0
            
            # Most effective recommendation type
            effective_types = recommendations.filter(helped_mood=True).values(
                'recommendation_type'
            ).annotate(
                count=Count('id')
            ).order_by('-count')
            
            if effective_types:
                analytics_data['most_effective_type'] = effective_types[0]['recommendation_type']
            
            # Emotion-music correlation
            emotions = recommendations.values('target_emotion').distinct()
            for emotion_data in emotions:
                emotion = emotion_data['target_emotion']
                emotion_recs = recommendations.filter(target_emotion=emotion)
                success_rate = emotion_recs.filter(helped_mood=True).count() / emotion_recs.count()
                analytics_data['emotion_music_correlation'][emotion] = round(success_rate, 2)
            
            # Therapeutic effectiveness
            therapeutic_recs = recommendations.filter(
                recommendation_type__in=['healing', 'calm_down', 'mood_boost']
            )
            if therapeutic_recs.exists():
                therapeutic_success = therapeutic_recs.filter(helped_mood=True).count()
                analytics_data['therapeutic_effectiveness'] = round(
                    (therapeutic_success / therapeutic_recs.count()) * 100, 2
                )
        
        serializer = MusicAnalyticsSerializer(data=analytics_data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        
        return Response(analytics_data, status=status.HTTP_200_OK)


class TherapeuticSoundViewSet(viewsets.ModelViewSet):
    """ViewSet for therapeutic sounds"""
    serializer_class = TherapeuticSoundSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get therapeutic sounds, filtered by category if specified"""
        queryset = TherapeuticSound.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by premium status
        if not self.request.user.is_premium:
            queryset = queryset.filter(is_premium=False)
        
        return queryset.order_by('-effectiveness_score')
    
    @action(detail=False, methods=['get'], url_path='categories')
    def categories(self, request):
        """Get available therapeutic sound categories"""
        categories = TherapeuticSound.SOUND_CATEGORIES
        return Response({
            'categories': [
                {
                    'value': cat[0],
                    'label': cat[1],
                    'count': TherapeuticSound.objects.filter(category=cat[0]).count()
                }
                for cat in categories
            ]
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='binaural')
    def binaural(self, request):
        """Get binaural beats for specific brainwave states"""
        brainwave = request.query_params.get('state', 'alpha')
        
        sounds = TherapeuticSound.objects.filter(
            category='binaural',
            brainwave_state=brainwave
        )
        
        serializer = TherapeuticSoundSerializer(sounds, many=True)
        return Response({
            'brainwave_state': brainwave,
            'sounds': serializer.data,
            'description': self._get_brainwave_description(brainwave)
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='play')
    def play(self, request, pk=None):
        """Record play event and update statistics"""
        sound = self.get_object()
        sound.play_count += 1
        sound.save()
        
        # Track in user's listening history
        # (Could create a listening history model here)
        
        return Response({
            'message': 'Play event recorded',
            'play_count': sound.play_count
        }, status=status.HTTP_200_OK)
    
    def _get_brainwave_description(self, state):
        """Get description for brainwave states"""
        descriptions = {
            'delta': 'Deep sleep and healing (0.5-4 Hz)',
            'theta': 'Deep meditation and REM sleep (4-8 Hz)',
            'alpha': 'Relaxation and creativity (8-13 Hz)',
            'beta': 'Focus and concentration (13-30 Hz)',
            'gamma': 'Peak awareness and cognition (30-100 Hz)'
        }
        return descriptions.get(state, 'Unknown brainwave state')