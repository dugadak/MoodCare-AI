"""
AI-powered music recommendation engine
"""
import openai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import random
from typing import Dict, List, Optional
from django.conf import settings
import numpy as np


class MusicRecommender:
    """Generate personalized music recommendations based on emotional state"""
    
    def __init__(self):
        # Initialize OpenAI
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Initialize Spotify (if credentials available)
        if hasattr(settings, 'SPOTIFY_CLIENT_ID'):
            auth = SpotifyClientCredentials(
                client_id=settings.SPOTIFY_CLIENT_ID,
                client_secret=settings.SPOTIFY_CLIENT_SECRET
            )
            self.spotify = spotipy.Spotify(auth_manager=auth)
        else:
            self.spotify = None
        
        # Emotion to music characteristic mapping
        self.emotion_music_map = {
            'joy': {
                'valence': (0.7, 1.0),  # High positivity
                'energy': (0.6, 0.9),
                'tempo': (120, 140),
                'genres': ['pop', 'dance', 'indie'],
                'characteristics': ['upbeat', 'cheerful', 'bright']
            },
            'sadness': {
                'valence': (0.0, 0.4),
                'energy': (0.2, 0.5),
                'tempo': (60, 90),
                'genres': ['classical', 'ambient', 'acoustic'],
                'characteristics': ['melancholic', 'gentle', 'soothing']
            },
            'anger': {
                'valence': (0.2, 0.5),
                'energy': (0.7, 1.0),
                'tempo': (130, 180),
                'genres': ['rock', 'metal', 'electronic'],
                'characteristics': ['intense', 'powerful', 'cathartic']
            },
            'fear': {
                'valence': (0.3, 0.6),
                'energy': (0.3, 0.6),
                'tempo': (70, 110),
                'genres': ['ambient', 'new age', 'classical'],
                'characteristics': ['calming', 'reassuring', 'peaceful']
            },
            'surprise': {
                'valence': (0.5, 0.8),
                'energy': (0.5, 0.8),
                'tempo': (100, 130),
                'genres': ['experimental', 'electronic', 'world'],
                'characteristics': ['unexpected', 'dynamic', 'interesting']
            },
            'disgust': {
                'valence': (0.4, 0.6),
                'energy': (0.4, 0.6),
                'tempo': (90, 120),
                'genres': ['alternative', 'indie', 'folk'],
                'characteristics': ['cleansing', 'refreshing', 'neutral']
            },
            'trust': {
                'valence': (0.5, 0.8),
                'energy': (0.4, 0.7),
                'tempo': (80, 120),
                'genres': ['soul', 'r&b', 'jazz'],
                'characteristics': ['warm', 'comforting', 'stable']
            },
            'anticipation': {
                'valence': (0.6, 0.9),
                'energy': (0.6, 0.9),
                'tempo': (110, 140),
                'genres': ['progressive', 'electronic', 'pop'],
                'characteristics': ['building', 'exciting', 'energizing']
            }
        }
        
        # Therapeutic music categories
        self.therapeutic_categories = {
            'mood_boost': {
                'description': 'Uplifting music to improve mood',
                'valence_boost': 0.2,
                'energy_boost': 0.1
            },
            'calm_down': {
                'description': 'Soothing music to reduce anxiety',
                'valence_target': 0.5,
                'energy_reduction': -0.3
            },
            'energize': {
                'description': 'Energizing music to increase motivation',
                'energy_boost': 0.3,
                'tempo_increase': 20
            },
            'focus': {
                'description': 'Music to enhance concentration',
                'valence_range': (0.5, 0.7),
                'energy_range': (0.4, 0.6),
                'instrumental': True
            },
            'sleep': {
                'description': 'Relaxing music for better sleep',
                'energy_max': 0.3,
                'tempo_max': 80,
                'instrumental': True
            },
            'healing': {
                'description': 'Therapeutic music for emotional healing',
                'genres': ['ambient', 'classical', 'nature'],
                'characteristics': ['peaceful', 'gentle', 'restorative']
            },
            'cathartic': {
                'description': 'Music for emotional release',
                'allow_intense': True,
                'emotional_range': 'wide'
            }
        }
    
    def get_recommendations(self,
                           current_emotion: str,
                           emotion_intensity: int,
                           target_emotion: Optional[str] = None,
                           recommendation_type: str = 'mood_boost',
                           preferences: Optional[Dict] = None) -> List[Dict]:
        """
        Generate music recommendations based on emotional state
        
        Args:
            current_emotion: Current emotional state
            emotion_intensity: Intensity of emotion (1-10)
            target_emotion: Desired emotional state
            recommendation_type: Type of recommendation
            preferences: User preferences (genres, artists, etc.)
        
        Returns:
            List of recommended tracks with metadata
        """
        
        # Get emotion characteristics
        emotion_profile = self.emotion_music_map.get(
            current_emotion, 
            self.emotion_music_map['trust']
        )
        
        # Adjust based on recommendation type
        if recommendation_type in self.therapeutic_categories:
            therapy_profile = self.therapeutic_categories[recommendation_type]
            emotion_profile = self._merge_profiles(emotion_profile, therapy_profile)
        
        # Generate recommendations
        if self.spotify:
            recommendations = self._get_spotify_recommendations(
                emotion_profile, preferences
            )
        else:
            recommendations = self._generate_mock_recommendations(
                emotion_profile, preferences
            )
        
        # Add AI-generated insights
        for rec in recommendations:
            rec['recommendation_reason'] = self._generate_recommendation_reason(
                rec, current_emotion, target_emotion, recommendation_type
            )
            rec['therapeutic_value'] = self._calculate_therapeutic_value(
                rec, current_emotion, target_emotion
            )
        
        return recommendations
    
    def _get_spotify_recommendations(self, profile: Dict, preferences: Optional[Dict]) -> List[Dict]:
        """Get recommendations from Spotify API"""
        try:
            # Build recommendation parameters
            params = {
                'limit': 10,
                'market': 'US',
                'target_valence': (profile['valence'][0] + profile['valence'][1]) / 2,
                'target_energy': (profile['energy'][0] + profile['energy'][1]) / 2,
                'target_tempo': (profile['tempo'][0] + profile['tempo'][1]) / 2
            }
            
            # Add seed genres
            if 'genres' in profile:
                available_genres = self.spotify.recommendation_genre_seeds()['genres']
                seed_genres = [g for g in profile['genres'] if g in available_genres][:3]
                if seed_genres:
                    params['seed_genres'] = seed_genres
            
            # Get recommendations
            results = self.spotify.recommendations(**params)
            
            recommendations = []
            for track in results['tracks']:
                # Get audio features
                audio_features = self.spotify.audio_features(track['id'])[0]
                
                rec = {
                    'track_id': track['id'],
                    'track_name': track['name'],
                    'artist': ', '.join([a['name'] for a in track['artists']]),
                    'album': track['album']['name'],
                    'preview_url': track.get('preview_url'),
                    'spotify_url': track['external_urls']['spotify'],
                    'audio_features': {
                        'valence': audio_features['valence'],
                        'energy': audio_features['energy'],
                        'tempo': audio_features['tempo'],
                        'danceability': audio_features['danceability'],
                        'instrumentalness': audio_features['instrumentalness'],
                        'acousticness': audio_features['acousticness']
                    },
                    'recommendation_score': self._calculate_recommendation_score(
                        audio_features, profile
                    )
                }
                recommendations.append(rec)
            
            # Sort by recommendation score
            recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
            
            return recommendations
            
        except Exception as e:
            print(f"Spotify API error: {str(e)}")
            return self._generate_mock_recommendations(profile, preferences)
    
    def _generate_mock_recommendations(self, profile: Dict, preferences: Optional[Dict]) -> List[Dict]:
        """Generate mock recommendations when Spotify is not available"""
        
        mock_tracks = [
            {
                'track_name': 'Weightless',
                'artist': 'Marconi Union',
                'genre': 'ambient',
                'valence': 0.3,
                'energy': 0.2,
                'therapeutic': True
            },
            {
                'track_name': 'River Flows in You',
                'artist': 'Yiruma',
                'genre': 'classical',
                'valence': 0.5,
                'energy': 0.3,
                'therapeutic': True
            },
            {
                'track_name': 'Happy',
                'artist': 'Pharrell Williams',
                'genre': 'pop',
                'valence': 0.9,
                'energy': 0.8,
                'therapeutic': False
            },
            {
                'track_name': 'Clair de Lune',
                'artist': 'Claude Debussy',
                'genre': 'classical',
                'valence': 0.4,
                'energy': 0.2,
                'therapeutic': True
            },
            {
                'track_name': 'Three Little Birds',
                'artist': 'Bob Marley',
                'genre': 'reggae',
                'valence': 0.8,
                'energy': 0.6,
                'therapeutic': True
            }
        ]
        
        # Filter based on profile
        target_valence = (profile['valence'][0] + profile['valence'][1]) / 2
        target_energy = (profile['energy'][0] + profile['energy'][1]) / 2
        
        recommendations = []
        for track in mock_tracks:
            # Calculate similarity score
            valence_diff = abs(track['valence'] - target_valence)
            energy_diff = abs(track['energy'] - target_energy)
            similarity_score = 1 - (valence_diff + energy_diff) / 2
            
            rec = {
                'track_id': f"mock_{track['track_name'].replace(' ', '_').lower()}",
                'track_name': track['track_name'],
                'artist': track['artist'],
                'album': 'Best Collection',
                'audio_features': {
                    'valence': track['valence'],
                    'energy': track['energy'],
                    'tempo': 100 + int(track['energy'] * 80),
                    'therapeutic': track['therapeutic']
                },
                'recommendation_score': similarity_score
            }
            recommendations.append(rec)
        
        # Sort by score and return top 5
        recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
        return recommendations[:5]
    
    def _merge_profiles(self, emotion_profile: Dict, therapy_profile: Dict) -> Dict:
        """Merge emotion and therapy profiles"""
        merged = emotion_profile.copy()
        
        # Adjust valence
        if 'valence_boost' in therapy_profile:
            merged['valence'] = (
                min(1.0, emotion_profile['valence'][0] + therapy_profile['valence_boost']),
                min(1.0, emotion_profile['valence'][1] + therapy_profile['valence_boost'])
            )
        
        # Adjust energy
        if 'energy_boost' in therapy_profile:
            merged['energy'] = (
                max(0.0, min(1.0, emotion_profile['energy'][0] + therapy_profile['energy_boost'])),
                max(0.0, min(1.0, emotion_profile['energy'][1] + therapy_profile['energy_boost']))
            )
        
        if 'energy_reduction' in therapy_profile:
            merged['energy'] = (
                max(0.0, emotion_profile['energy'][0] + therapy_profile['energy_reduction']),
                max(0.0, emotion_profile['energy'][1] + therapy_profile['energy_reduction'])
            )
        
        # Override with specific ranges
        if 'valence_range' in therapy_profile:
            merged['valence'] = therapy_profile['valence_range']
        
        if 'energy_range' in therapy_profile:
            merged['energy'] = therapy_profile['energy_range']
        
        return merged
    
    def _calculate_recommendation_score(self, features: Dict, profile: Dict) -> float:
        """Calculate how well a track matches the desired profile"""
        score = 0.0
        weights = {'valence': 0.4, 'energy': 0.3, 'tempo': 0.2, 'other': 0.1}
        
        # Valence match
        if profile.get('valence'):
            target = (profile['valence'][0] + profile['valence'][1]) / 2
            valence_score = 1 - abs(features.get('valence', 0.5) - target)
            score += valence_score * weights['valence']
        
        # Energy match
        if profile.get('energy'):
            target = (profile['energy'][0] + profile['energy'][1]) / 2
            energy_score = 1 - abs(features.get('energy', 0.5) - target)
            score += energy_score * weights['energy']
        
        # Tempo match
        if profile.get('tempo'):
            target = (profile['tempo'][0] + profile['tempo'][1]) / 2
            tempo_diff = abs(features.get('tempo', 100) - target) / 100
            tempo_score = max(0, 1 - tempo_diff)
            score += tempo_score * weights['tempo']
        
        return round(score, 2)
    
    def _generate_recommendation_reason(self, track: Dict, current_emotion: str,
                                       target_emotion: Optional[str], 
                                       recommendation_type: str) -> str:
        """Generate AI explanation for why this track was recommended"""
        
        features = track.get('audio_features', {})
        
        reasons = []
        
        # Valence-based reasoning
        if features.get('valence', 0) > 0.7:
            reasons.append("This uplifting track can help boost your mood")
        elif features.get('valence', 0) < 0.3:
            reasons.append("This gentle melody matches your current emotional state")
        
        # Energy-based reasoning
        if features.get('energy', 0) > 0.7:
            reasons.append("The high energy can help energize and motivate you")
        elif features.get('energy', 0) < 0.3:
            reasons.append("The calming energy promotes relaxation")
        
        # Recommendation type specific
        if recommendation_type == 'sleep':
            reasons.append("Perfect for winding down before sleep")
        elif recommendation_type == 'focus':
            reasons.append("Helps maintain concentration without distraction")
        elif recommendation_type == 'healing':
            reasons.append("Therapeutic qualities for emotional processing")
        
        # Emotion transition
        if target_emotion and target_emotion != current_emotion:
            reasons.append(f"Helps transition from {current_emotion} to {target_emotion}")
        
        return ". ".join(reasons) if reasons else "Recommended based on your emotional profile"
    
    def _calculate_therapeutic_value(self, track: Dict, current_emotion: str,
                                    target_emotion: Optional[str]) -> float:
        """Calculate the therapeutic value of a track"""
        
        features = track.get('audio_features', {})
        value = 0.5  # Base value
        
        # Mood improvement potential
        if current_emotion in ['sadness', 'anger', 'fear']:
            if features.get('valence', 0) > 0.6:
                value += 0.2
        
        # Calming effect
        if current_emotion in ['anger', 'fear', 'anxiety']:
            if features.get('energy', 0) < 0.4:
                value += 0.15
        
        # Instrumental bonus (less cognitive load)
        if features.get('instrumentalness', 0) > 0.5:
            value += 0.1
        
        # Acoustic bonus (natural, soothing)
        if features.get('acousticness', 0) > 0.5:
            value += 0.05
        
        return min(1.0, value)