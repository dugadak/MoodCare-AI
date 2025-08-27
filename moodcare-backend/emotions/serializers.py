from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Emotion, EmotionImage, EmotionRecord

User = get_user_model()


class EmotionImageSerializer(serializers.ModelSerializer):
    """Emotion image serializer"""
    
    class Meta:
        model = EmotionImage
        fields = ('id', 'image', 'caption', 'created_at')
        read_only_fields = ('id', 'created_at')


class EmotionSerializer(serializers.ModelSerializer):
    """Emotion serializer"""
    
    images = EmotionImageSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Emotion
        fields = (
            'id', 'user', 'emotion_type', 'intensity', 'note',
            'voice_note_url', 'location', 'activity', 'people',
            'weather', 'physical_state', 'ai_analysis',
            'sentiment_score', 'triggers', 'images',
            'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'user', 'ai_analysis', 'sentiment_score',
            'created_at', 'updated_at'
        )
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class EmotionListSerializer(serializers.ModelSerializer):
    """Emotion list serializer (simplified)"""
    
    class Meta:
        model = Emotion
        fields = (
            'id', 'emotion_type', 'intensity', 
            'note', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class EmotionAnalysisRequestSerializer(serializers.Serializer):
    """Serializer for emotion analysis requests"""
    text = serializers.CharField(max_length=5000, required=False, allow_blank=True)
    audio = serializers.FileField(required=False)
    context = serializers.JSONField(required=False, default=dict)
    language = serializers.CharField(max_length=10, default='ko-KR')
    
    def validate(self, data):
        """Ensure at least text or audio is provided"""
        if not data.get('text') and not data.get('audio'):
            raise serializers.ValidationError(
                "Either text or audio must be provided for analysis"
            )
        return data


class EmotionStatisticsSerializer(serializers.Serializer):
    """Serializer for emotion statistics"""
    emotion_distribution = serializers.DictField()
    average_intensity = serializers.FloatField()
    total_records = serializers.IntegerField()
    dominant_emotion = serializers.CharField()
    emotional_volatility = serializers.FloatField()
    trend = serializers.CharField()
    period = serializers.CharField()
    

class EmotionInsightSerializer(serializers.Serializer):
    """Serializer for AI-generated insights"""
    overall_state = serializers.CharField()
    patterns = serializers.ListField(child=serializers.CharField())
    triggers = serializers.ListField(child=serializers.CharField())
    indicators = serializers.ListField(child=serializers.CharField())
    recommendations = serializers.ListField(child=serializers.CharField())
    concerns = serializers.ListField(child=serializers.CharField())
    statistics = serializers.DictField()
    generated_at = serializers.DateTimeField()


class EmotionTrendSerializer(serializers.Serializer):
    """Serializer for emotion trends over time"""
    date = serializers.DateField()
    emotion = serializers.CharField()
    intensity = serializers.FloatField()
    count = serializers.IntegerField()
    sentiment_score = serializers.FloatField()


class VoiceAnalysisResponseSerializer(serializers.Serializer):
    """Response serializer for voice emotion analysis"""
    transcribed_text = serializers.CharField()
    primary_emotion = serializers.CharField()
    intensity = serializers.IntegerField()
    sentiment_score = serializers.FloatField()
    voice_features = serializers.DictField()
    analysis_result = serializers.DictField()
    suggestions = serializers.ListField(child=serializers.CharField())