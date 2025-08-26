from django.db import models
from django.conf import settings


class Emotion(models.Model):
    """Emotion record model"""
    
    EMOTION_TYPES = [
        ('joy', 'Joy'),
        ('sadness', 'Sadness'),
        ('anger', 'Anger'),
        ('fear', 'Fear'),
        ('surprise', 'Surprise'),
        ('disgust', 'Disgust'),
        ('trust', 'Trust'),
        ('anticipation', 'Anticipation'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emotions')
    emotion_type = models.CharField(max_length=20, choices=EMOTION_TYPES)
    intensity = models.IntegerField(default=5)  # 1-10 scale
    note = models.TextField(blank=True)
    voice_note_url = models.URLField(blank=True, null=True)
    
    # Context
    location = models.CharField(max_length=100, blank=True)
    activity = models.CharField(max_length=100, blank=True)
    people = models.CharField(max_length=100, blank=True)
    weather = models.CharField(max_length=50, blank=True)
    physical_state = models.CharField(max_length=50, blank=True)
    
    # AI Analysis
    ai_analysis = models.JSONField(default=dict, blank=True)
    sentiment_score = models.FloatField(blank=True, null=True)
    
    # Triggers
    triggers = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'emotions'
        ordering = ['-created_at']
        verbose_name = 'Emotion'
        verbose_name_plural = 'Emotions'
    
    def __str__(self):
        return f"{self.user.username} - {self.emotion_type} ({self.created_at})"


class EmotionImage(models.Model):
    """Images attached to emotion records"""
    
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='emotions/')
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'emotion_images'
        verbose_name = 'Emotion Image'
        verbose_name_plural = 'Emotion Images'