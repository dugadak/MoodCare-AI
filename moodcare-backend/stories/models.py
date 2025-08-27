from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Story(models.Model):
    """Interactive AI-generated story model"""
    
    STORY_TYPES = [
        ('healing', 'Healing Story'),
        ('adventure', 'Adventure Story'),
        ('meditation', 'Meditation Journey'),
        ('fantasy', 'Fantasy Tale'),
        ('personal', 'Personal Growth')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(max_length=255)
    content = models.TextField()
    story_type = models.CharField(max_length=20, choices=STORY_TYPES, default='healing')
    
    # Emotion context
    emotion_context = models.JSONField(default=dict)  # Current user emotion state
    emotion_tags = models.JSONField(default=list)  # Target emotions for the story
    
    # Interactive elements
    current_chapter = models.IntegerField(default=1)
    choices_made = models.JSONField(default=list)
    story_branches = models.JSONField(default=dict)  # Stores different story paths
    
    # Metadata
    reading_time = models.IntegerField(help_text="Estimated reading time in minutes")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['story_type', 'is_completed']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"

class StoryInteraction(models.Model):
    """Track user interactions with stories"""
    
    INTERACTION_TYPES = [
        ('choice', 'Story Choice'),
        ('reaction', 'Emotional Reaction'),
        ('bookmark', 'Bookmark'),
        ('highlight', 'Text Highlight'),
        ('note', 'User Note')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    chapter = models.IntegerField()
    
    # Interaction data
    choice_id = models.CharField(max_length=50, null=True, blank=True)
    choice_text = models.TextField(null=True, blank=True)
    reaction = models.CharField(max_length=50, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['story', 'chapter', 'created_at']
    
    def __str__(self):
        return f"{self.interaction_type} - {self.story.title}"

class StoryTemplate(models.Model):
    """Pre-defined story templates for different emotional states"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    story_type = models.CharField(max_length=20, choices=Story.STORY_TYPES)
    
    # Template structure
    template_structure = models.JSONField()  # Defines story flow and branches
    target_emotions = models.JSONField(default=list)
    
    # Usage stats
    usage_count = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-usage_count']
    
    def __str__(self):
        return self.name