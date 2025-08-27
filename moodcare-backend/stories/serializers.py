from rest_framework import serializers
from .models import Story, StoryInteraction, StoryTemplate


class StorySerializer(serializers.ModelSerializer):
    """Serializer for Story model"""
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Story
        fields = [
            'id', 'user', 'title', 'content', 'story_type',
            'emotion_context', 'emotion_tags', 'current_chapter',
            'choices_made', 'story_branches', 'reading_time',
            'is_completed', 'created_at', 'updated_at', 'last_read_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StoryCreateRequestSerializer(serializers.Serializer):
    """Serializer for story generation request"""
    story_type = serializers.ChoiceField(choices=Story.STORY_TYPES)
    current_emotion = serializers.CharField(max_length=50)
    emotion_intensity = serializers.IntegerField(min_value=1, max_value=10)
    target_emotion = serializers.CharField(max_length=50, required=False)
    preferences = serializers.JSONField(required=False, default=dict)
    length = serializers.ChoiceField(
        choices=['short', 'medium', 'long'],
        default='medium'
    )


class StoryInteractionSerializer(serializers.ModelSerializer):
    """Serializer for story interactions"""
    
    class Meta:
        model = StoryInteraction
        fields = [
            'id', 'story', 'user', 'interaction_type', 'chapter',
            'choice_id', 'choice_text', 'reaction', 'note', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'user']


class StoryChoiceSerializer(serializers.Serializer):
    """Serializer for story choices"""
    choice_id = serializers.CharField(max_length=50)
    choice_text = serializers.CharField()
    next_chapter = serializers.IntegerField()
    emotion_impact = serializers.DictField(required=False)


class StoryGenerationResponseSerializer(serializers.Serializer):
    """Response serializer for story generation"""
    story_id = serializers.UUIDField()
    title = serializers.CharField()
    first_chapter = serializers.CharField()
    choices = StoryChoiceSerializer(many=True, required=False)
    estimated_reading_time = serializers.IntegerField()
    emotion_journey = serializers.ListField(child=serializers.CharField())


class StoryTemplateSerializer(serializers.ModelSerializer):
    """Serializer for story templates"""
    
    class Meta:
        model = StoryTemplate
        fields = [
            'id', 'name', 'description', 'story_type', 'template_structure',
            'target_emotions', 'usage_count', 'success_rate', 'is_active'
        ]
        read_only_fields = ['id', 'usage_count', 'success_rate']


class StoryProgressSerializer(serializers.Serializer):
    """Serializer for story reading progress"""
    story_id = serializers.UUIDField()
    current_chapter = serializers.IntegerField()
    total_chapters = serializers.IntegerField()
    completion_percentage = serializers.FloatField()
    choices_made = serializers.ListField(child=serializers.DictField())
    emotional_arc = serializers.ListField(child=serializers.CharField())
    time_spent = serializers.IntegerField()  # in minutes