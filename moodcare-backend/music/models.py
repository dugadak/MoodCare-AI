from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class MusicProfile(models.Model):
    """User's musical preference and emotion mapping profile"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='music_profile')
    
    # Emotion-Music Mapping (learned from user behavior)
    emotion_music_map = models.JSONField(default=dict)  # {emotion: {genres: [], artists: [], features: {}}}
    
    # Preferred music characteristics
    preferred_genres = models.JSONField(default=list)
    preferred_artists = models.JSONField(default=list)
    preferred_energy_level = models.FloatField(default=0.5)  # 0-1 scale
    preferred_tempo = models.IntegerField(default=120)  # BPM
    
    # Listening patterns
    peak_listening_hours = models.JSONField(default=list)  # Hours when user listens most
    listening_context = models.JSONField(default=dict)  # {context: music_preferences}
    
    # Advanced preferences
    music_for_emotions = models.JSONField(default=dict)  # {emotion: [track_ids]}
    healing_playlist = models.JSONField(default=list)  # Tracks that improved mood
    trigger_songs = models.JSONField(default=list)  # Songs to avoid during certain emotions
    
    # Biometric response (future feature)
    heart_rate_response = models.JSONField(default=dict)  # Track ID to heart rate change
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Music Profile - {self.user.username}"

class MusicRecommendation(models.Model):
    """AI-generated music recommendations based on emotional state"""
    
    RECOMMENDATION_TYPES = [
        ('mood_boost', 'Mood Booster'),
        ('calm_down', 'Calming'),
        ('energize', 'Energizing'),
        ('focus', 'Focus Enhancement'),
        ('sleep', 'Sleep Aid'),
        ('healing', 'Emotional Healing'),
        ('cathartic', 'Emotional Release')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='music_recommendations')
    
    # Emotion context
    emotion_trigger = models.ForeignKey('emotions.EmotionRecord', on_delete=models.SET_NULL, null=True)
    target_emotion = models.CharField(max_length=50)
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPES)
    
    # Music data
    track_id = models.CharField(max_length=255)  # Spotify/YouTube ID
    track_name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, null=True, blank=True)
    
    # Audio features (from Spotify API)
    audio_features = models.JSONField(default=dict)  # energy, valence, danceability, etc.
    
    # Recommendation metadata
    recommendation_score = models.FloatField()  # AI confidence score
    recommendation_reason = models.TextField()  # Why this song was recommended
    
    # User feedback
    user_rating = models.IntegerField(null=True, blank=True)  # 1-5 stars
    helped_mood = models.BooleanField(null=True, blank=True)
    skipped = models.BooleanField(default=False)
    play_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    played_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['recommendation_type', 'recommendation_score']),
        ]
    
    def __str__(self):
        return f"{self.track_name} - {self.user.username}"

class MusicDiary(models.Model):
    """Daily music diary linking emotions to songs"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='music_diaries')
    date = models.DateField()
    
    # Daily soundtrack
    morning_track = models.ForeignKey(MusicRecommendation, on_delete=models.SET_NULL, 
                                     null=True, related_name='morning_diaries')
    afternoon_track = models.ForeignKey(MusicRecommendation, on_delete=models.SET_NULL,
                                       null=True, related_name='afternoon_diaries')
    evening_track = models.ForeignKey(MusicRecommendation, on_delete=models.SET_NULL,
                                     null=True, related_name='evening_diaries')
    
    # Emotional journey through music
    emotional_arc = models.JSONField(default=list)  # [{time, emotion, track_id, intensity}]
    
    # Day summary
    dominant_emotion = models.CharField(max_length=50)
    energy_level = models.FloatField()  # Average energy throughout the day
    
    # Musical medicine prescribed
    therapeutic_playlist = models.JSONField(default=list)  # Curated healing playlist
    
    # Notes
    reflection = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"Music Diary - {self.user.username} - {self.date}"

class AudioVisualization(models.Model):
    """Store audio visualization data for real-time display"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Source
    source_type = models.CharField(max_length=20)  # 'voice', 'music', 'ambient'
    source_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Visualization data
    waveform_data = models.JSONField()  # Array of amplitude values
    frequency_spectrum = models.JSONField()  # FFT data
    emotion_colors = models.JSONField()  # Color mapping based on emotion
    
    # 3D visualization parameters
    particle_system = models.JSONField(default=dict)  # 3D particle animation data
    emotion_geometry = models.JSONField(default=dict)  # 3D shape based on emotion
    
    # Animation
    animation_preset = models.CharField(max_length=50)
    animation_speed = models.FloatField(default=1.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Audio Viz - {self.user.username} - {self.source_type}"

class TherapeuticSound(models.Model):
    """Curated therapeutic sounds and ASMR content"""
    
    SOUND_CATEGORIES = [
        ('nature', 'Nature Sounds'),
        ('white_noise', 'White Noise'),
        ('binaural', 'Binaural Beats'),
        ('asmr', 'ASMR'),
        ('meditation', 'Meditation'),
        ('breathing', 'Breathing Exercises')
    ]
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=SOUND_CATEGORIES)
    description = models.TextField()
    
    # Audio file
    audio_url = models.URLField()
    duration = models.IntegerField(help_text="Duration in seconds")
    
    # Therapeutic properties
    target_emotions = models.JSONField(default=list)
    benefits = models.JSONField(default=list)
    
    # Binaural beat specific
    frequency = models.FloatField(null=True, blank=True, help_text="Hz for binaural beats")
    brainwave_state = models.CharField(max_length=20, null=True, blank=True)  # alpha, theta, delta
    
    # Usage stats
    play_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    effectiveness_score = models.FloatField(default=0.0)  # Based on mood improvement
    
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-effectiveness_score', '-play_count']
    
    def __str__(self):
        return f"{self.name} ({self.category})"