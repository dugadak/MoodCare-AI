from rest_framework import serializers
from .models import (
    MusicProfile, MusicRecommendation, MusicDiary,
    AudioVisualization, TherapeuticSound
)


class MusicProfileSerializer(serializers.ModelSerializer):
    """Serializer for user music profile"""
    
    class Meta:
        model = MusicProfile
        fields = [
            'id', 'user', 'emotion_music_map', 'preferred_genres',
            'preferred_artists', 'preferred_energy_level', 'preferred_tempo',
            'peak_listening_hours', 'listening_context', 'music_for_emotions',
            'healing_playlist', 'trigger_songs', 'heart_rate_response',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class MusicRecommendationSerializer(serializers.ModelSerializer):
    """Serializer for music recommendations"""
    
    class Meta:
        model = MusicRecommendation
        fields = [
            'id', 'user', 'emotion_trigger', 'target_emotion',
            'recommendation_type', 'track_id', 'track_name', 'artist',
            'album', 'audio_features', 'recommendation_score',
            'recommendation_reason', 'user_rating', 'helped_mood',
            'skipped', 'play_count', 'created_at', 'played_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class MusicRecommendationRequestSerializer(serializers.Serializer):
    """Request serializer for music recommendations"""
    current_emotion = serializers.CharField(max_length=50)
    emotion_intensity = serializers.IntegerField(min_value=1, max_value=10)
    target_emotion = serializers.CharField(max_length=50, required=False)
    recommendation_type = serializers.ChoiceField(
        choices=MusicRecommendation.RECOMMENDATION_TYPES,
        default='mood_boost'
    )
    genre_preference = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    energy_level = serializers.FloatField(min_value=0, max_value=1, required=False)
    context = serializers.CharField(max_length=50, required=False)  # work, exercise, sleep, etc.


class MusicDiarySerializer(serializers.ModelSerializer):
    """Serializer for music diary entries"""
    morning_track_detail = MusicRecommendationSerializer(
        source='morning_track', read_only=True
    )
    afternoon_track_detail = MusicRecommendationSerializer(
        source='afternoon_track', read_only=True
    )
    evening_track_detail = MusicRecommendationSerializer(
        source='evening_track', read_only=True
    )
    
    class Meta:
        model = MusicDiary
        fields = [
            'id', 'user', 'date', 'morning_track', 'afternoon_track',
            'evening_track', 'morning_track_detail', 'afternoon_track_detail',
            'evening_track_detail', 'emotional_arc', 'dominant_emotion',
            'energy_level', 'therapeutic_playlist', 'reflection', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class AudioVisualizationSerializer(serializers.ModelSerializer):
    """Serializer for audio visualization data"""
    
    class Meta:
        model = AudioVisualization
        fields = [
            'id', 'user', 'source_type', 'source_id', 'waveform_data',
            'frequency_spectrum', 'emotion_colors', 'particle_system',
            'emotion_geometry', 'animation_preset', 'animation_speed',
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class TherapeuticSoundSerializer(serializers.ModelSerializer):
    """Serializer for therapeutic sounds"""
    
    class Meta:
        model = TherapeuticSound
        fields = [
            'id', 'name', 'category', 'description', 'audio_url',
            'duration', 'target_emotions', 'benefits', 'frequency',
            'brainwave_state', 'play_count', 'average_rating',
            'effectiveness_score', 'is_premium', 'created_at'
        ]
        read_only_fields = ['id', 'play_count', 'average_rating', 'effectiveness_score']


class PlaylistGenerationRequestSerializer(serializers.Serializer):
    """Request serializer for playlist generation"""
    emotion = serializers.CharField(max_length=50)
    duration = serializers.IntegerField(min_value=5, max_value=120, default=30)  # minutes
    activity = serializers.CharField(max_length=50, required=False)
    include_therapeutic = serializers.BooleanField(default=False)
    include_binaural = serializers.BooleanField(default=False)


class MusicFeedbackSerializer(serializers.Serializer):
    """Serializer for music feedback"""
    track_id = serializers.CharField(max_length=255)
    rating = serializers.IntegerField(min_value=1, max_value=5)
    helped_mood = serializers.BooleanField()
    skipped = serializers.BooleanField(default=False)
    skip_reason = serializers.CharField(max_length=100, required=False)
    listened_duration = serializers.IntegerField(required=False)  # seconds


class MusicAnalyticsSerializer(serializers.Serializer):
    """Serializer for music analytics"""
    period = serializers.CharField(max_length=20)
    total_listening_time = serializers.IntegerField()  # minutes
    favorite_genre = serializers.CharField()
    favorite_artist = serializers.CharField()
    mood_improvement_rate = serializers.FloatField()
    most_effective_type = serializers.CharField()
    emotion_music_correlation = serializers.DictField()
    listening_patterns = serializers.DictField()
    therapeutic_effectiveness = serializers.FloatField()