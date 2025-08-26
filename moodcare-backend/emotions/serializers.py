from rest_framework import serializers
from .models import Emotion, EmotionImage


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