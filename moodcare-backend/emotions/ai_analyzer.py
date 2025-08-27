"""
AI-powered emotion analysis module
"""
import openai
import json
import numpy as np
from typing import Dict, List, Optional
from django.conf import settings
import speech_recognition as sr
from pydub import AudioSegment
import io
import tempfile
import os

class EmotionAnalyzer:
    """Advanced emotion analysis using GPT-4 and speech recognition"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.recognizer = sr.Recognizer()
        
        # Emotion categories and their characteristics
        self.emotion_categories = {
            'joy': ['happy', 'excited', 'cheerful', 'delighted', 'content'],
            'sadness': ['sad', 'depressed', 'melancholy', 'lonely', 'disappointed'],
            'anger': ['angry', 'frustrated', 'irritated', 'annoyed', 'furious'],
            'fear': ['afraid', 'anxious', 'worried', 'nervous', 'scared'],
            'surprise': ['surprised', 'amazed', 'astonished', 'shocked'],
            'disgust': ['disgusted', 'repulsed', 'revolted', 'appalled'],
            'trust': ['trusting', 'secure', 'confident', 'comfortable'],
            'anticipation': ['excited', 'eager', 'hopeful', 'expectant']
        }
    
    def analyze_text(self, text: str, context: Optional[Dict] = None) -> Dict:
        """
        Analyze emotions from text input using GPT-4
        
        Args:
            text: Input text to analyze
            context: Optional context information (location, activity, etc.)
        
        Returns:
            Dictionary containing emotion analysis results
        """
        try:
            # Prepare context for better analysis
            context_str = ""
            if context:
                context_str = f"\nContext: Location: {context.get('location', 'unknown')}, "
                context_str += f"Activity: {context.get('activity', 'unknown')}, "
                context_str += f"Weather: {context.get('weather', 'unknown')}"
            
            # Create prompt for GPT-4
            prompt = f"""
            Analyze the following text for emotional content. {context_str}
            
            Text: "{text}"
            
            Please provide:
            1. Primary emotion (from: joy, sadness, anger, fear, surprise, disgust, trust, anticipation)
            2. Emotion intensity (1-10 scale)
            3. Secondary emotions present
            4. Emotional triggers identified
            5. Brief psychological insight
            6. Suggested coping strategies (if negative emotions)
            
            Return the analysis in JSON format with keys:
            primary_emotion, intensity, secondary_emotions[], triggers[], insight, suggestions[]
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert psychologist and emotion analyst."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse GPT-4 response
            analysis = json.loads(response.choices[0].message.content)
            
            # Add sentiment score
            analysis['sentiment_score'] = self._calculate_sentiment_score(
                analysis['primary_emotion'], 
                analysis['intensity']
            )
            
            # Add emotional complexity score
            analysis['emotional_complexity'] = len(analysis.get('secondary_emotions', []))
            
            # Add timestamp and raw text
            from datetime import datetime
            analysis['analyzed_at'] = datetime.now().isoformat()
            analysis['raw_text'] = text
            analysis['context'] = context
            
            return analysis
            
        except Exception as e:
            print(f"Error in text emotion analysis: {str(e)}")
            return {
                'error': str(e),
                'primary_emotion': 'neutral',
                'intensity': 5,
                'sentiment_score': 0
            }
    
    def analyze_voice(self, audio_file, language='ko-KR') -> Dict:
        """
        Analyze emotions from voice input
        
        Args:
            audio_file: Audio file object or path
            language: Language code for speech recognition
        
        Returns:
            Dictionary containing emotion analysis from transcribed speech
        """
        try:
            # Convert audio to text
            text = self._transcribe_audio(audio_file, language)
            
            if not text:
                return {
                    'error': 'Could not transcribe audio',
                    'primary_emotion': 'neutral',
                    'intensity': 5
                }
            
            # Analyze voice characteristics
            voice_features = self._analyze_voice_features(audio_file)
            
            # Perform text-based emotion analysis
            text_analysis = self.analyze_text(text)
            
            # Combine text and voice analysis
            combined_analysis = {
                **text_analysis,
                'transcribed_text': text,
                'voice_features': voice_features,
                'source': 'voice',
                'language': language
            }
            
            # Adjust intensity based on voice features
            if voice_features:
                combined_intensity = (
                    text_analysis.get('intensity', 5) * 0.7 + 
                    voice_features.get('energy_level', 5) * 0.3
                )
                combined_analysis['intensity'] = round(combined_intensity)
            
            return combined_analysis
            
        except Exception as e:
            print(f"Error in voice emotion analysis: {str(e)}")
            return {
                'error': str(e),
                'primary_emotion': 'neutral',
                'intensity': 5
            }
    
    def _transcribe_audio(self, audio_file, language='ko-KR') -> str:
        """Transcribe audio to text using speech recognition"""
        try:
            # Save audio to temporary file if needed
            if hasattr(audio_file, 'read'):
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                    tmp_file.write(audio_file.read())
                    tmp_path = tmp_file.name
            else:
                tmp_path = audio_file
            
            # Convert to WAV if needed
            audio = AudioSegment.from_file(tmp_path)
            wav_path = tmp_path.replace(os.path.splitext(tmp_path)[1], '.wav')
            audio.export(wav_path, format='wav')
            
            # Use speech recognition
            with sr.AudioFile(wav_path) as source:
                audio_data = self.recognizer.record(source)
                
                # Try Google Speech Recognition first
                try:
                    text = self.recognizer.recognize_google(
                        audio_data, 
                        language=language
                    )
                except:
                    # Fallback to OpenAI Whisper
                    with open(wav_path, 'rb') as audio:
                        transcript = self.client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio,
                            language=language[:2]  # Use two-letter code for Whisper
                        )
                        text = transcript.text
            
            # Clean up temporary files
            if hasattr(audio_file, 'read'):
                os.unlink(tmp_path)
            if os.path.exists(wav_path) and wav_path != tmp_path:
                os.unlink(wav_path)
            
            return text
            
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return ""
    
    def _analyze_voice_features(self, audio_file) -> Dict:
        """Analyze voice characteristics for emotional cues"""
        try:
            import librosa
            
            # Load audio
            if hasattr(audio_file, 'read'):
                audio_file.seek(0)
                y, sr = librosa.load(io.BytesIO(audio_file.read()), sr=None)
            else:
                y, sr = librosa.load(audio_file, sr=None)
            
            # Extract features
            features = {}
            
            # Pitch analysis
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            features['pitch_mean'] = float(np.mean(pitches[pitches > 0]))
            features['pitch_std'] = float(np.std(pitches[pitches > 0]))
            
            # Energy/Volume
            features['energy_mean'] = float(np.mean(librosa.feature.rms(y=y)))
            features['energy_std'] = float(np.std(librosa.feature.rms(y=y)))
            features['energy_level'] = min(10, max(1, int(features['energy_mean'] * 20)))
            
            # Tempo
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            features['tempo'] = float(tempo)
            
            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
            features['brightness'] = float(np.mean(spectral_centroids))
            
            # Zero crossing rate (indicates speech vs silence)
            zcr = librosa.feature.zero_crossing_rate(y)
            features['speech_rate'] = float(np.mean(zcr))
            
            return features
            
        except Exception as e:
            print(f"Error analyzing voice features: {str(e)}")
            return {}
    
    def _calculate_sentiment_score(self, emotion: str, intensity: int) -> float:
        """
        Calculate sentiment score from -1 (negative) to 1 (positive)
        """
        positive_emotions = ['joy', 'trust', 'anticipation']
        negative_emotions = ['sadness', 'anger', 'fear', 'disgust']
        neutral_emotions = ['surprise']
        
        base_score = 0
        if emotion in positive_emotions:
            base_score = 1
        elif emotion in negative_emotions:
            base_score = -1
        elif emotion in neutral_emotions:
            base_score = 0
        
        # Adjust by intensity (1-10 scale)
        adjusted_score = base_score * (intensity / 10)
        
        return round(adjusted_score, 2)
    
    def get_emotion_insights(self, emotion_records: List[Dict]) -> Dict:
        """
        Generate insights from multiple emotion records
        
        Args:
            emotion_records: List of emotion analysis results
        
        Returns:
            Dictionary containing patterns and insights
        """
        if not emotion_records:
            return {'message': 'No emotion records to analyze'}
        
        try:
            # Prepare data for analysis
            emotions_data = {
                'emotions': [r.get('primary_emotion', 'neutral') for r in emotion_records],
                'intensities': [r.get('intensity', 5) for r in emotion_records],
                'sentiments': [r.get('sentiment_score', 0) for r in emotion_records],
                'timestamps': [r.get('analyzed_at', '') for r in emotion_records]
            }
            
            prompt = f"""
            Analyze the following emotional pattern data and provide psychological insights:
            
            Emotions recorded: {emotions_data['emotions']}
            Intensities: {emotions_data['intensities']}
            Sentiment scores: {emotions_data['sentiments']}
            
            Please provide:
            1. Overall emotional state assessment
            2. Identified patterns or cycles
            3. Potential triggers
            4. Mental health indicators
            5. Personalized recommendations
            6. Areas of concern (if any)
            
            Return as JSON with keys:
            overall_state, patterns[], triggers[], indicators[], recommendations[], concerns[]
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert psychologist analyzing emotional patterns."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=600
            )
            
            insights = json.loads(response.choices[0].message.content)
            
            # Add statistical analysis
            insights['statistics'] = {
                'most_common_emotion': max(set(emotions_data['emotions']), 
                                          key=emotions_data['emotions'].count),
                'average_intensity': round(np.mean(emotions_data['intensities']), 2),
                'average_sentiment': round(np.mean(emotions_data['sentiments']), 2),
                'emotional_volatility': round(np.std(emotions_data['intensities']), 2)
            }
            
            return insights
            
        except Exception as e:
            print(f"Error generating insights: {str(e)}")
            return {'error': str(e)}