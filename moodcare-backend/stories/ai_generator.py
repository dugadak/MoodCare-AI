"""
AI Story Generator using GPT-4
"""
import openai
import json
from typing import Dict, List, Optional
from django.conf import settings
import random


class StoryGenerator:
    """Generate interactive stories based on emotional context"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Story templates for different emotions
        self.emotion_themes = {
            'joy': ['celebration', 'achievement', 'friendship', 'discovery'],
            'sadness': ['healing', 'acceptance', 'hope', 'transformation'],
            'anger': ['resolution', 'understanding', 'forgiveness', 'empowerment'],
            'fear': ['courage', 'safety', 'protection', 'overcoming'],
            'surprise': ['adventure', 'mystery', 'wonder', 'exploration'],
            'disgust': ['cleansing', 'renewal', 'clarity', 'boundaries'],
            'trust': ['connection', 'loyalty', 'support', 'reliability'],
            'anticipation': ['journey', 'preparation', 'excitement', 'possibility']
        }
        
        self.story_lengths = {
            'short': (500, 1000),    # 500-1000 words
            'medium': (1000, 2000),   # 1000-2000 words
            'long': (2000, 4000)      # 2000-4000 words
        }
    
    def generate_story(self, 
                      story_type: str,
                      current_emotion: str,
                      emotion_intensity: int,
                      target_emotion: Optional[str] = None,
                      preferences: Optional[Dict] = None,
                      length: str = 'medium') -> Dict:
        """
        Generate a personalized story based on emotional state
        
        Args:
            story_type: Type of story (healing, adventure, etc.)
            current_emotion: User's current emotional state
            emotion_intensity: Intensity of current emotion (1-10)
            target_emotion: Desired emotional state after reading
            preferences: User preferences (themes, characters, etc.)
            length: Story length (short, medium, long)
        
        Returns:
            Dictionary containing story content and metadata
        """
        
        # Select appropriate themes
        themes = self.emotion_themes.get(current_emotion, ['journey'])
        selected_theme = random.choice(themes)
        
        # Determine word count
        min_words, max_words = self.story_lengths[length]
        
        # Build story prompt
        prompt = self._build_story_prompt(
            story_type, current_emotion, emotion_intensity,
            target_emotion, selected_theme, preferences, min_words, max_words
        )
        
        try:
            # Generate story with GPT-4
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a master storyteller and therapeutic narrative designer. Create immersive, emotionally intelligent stories that help people process and transform their emotions."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.8,
                max_tokens=4000
            )
            
            # Parse response
            story_data = json.loads(response.choices[0].message.content)
            
            # Add metadata
            story_data['theme'] = selected_theme
            story_data['word_count'] = len(story_data.get('content', '').split())
            story_data['reading_time'] = story_data['word_count'] // 200  # Average reading speed
            
            # Generate interactive choices if not present
            if 'choices' not in story_data and story_type in ['adventure', 'fantasy']:
                story_data['choices'] = self._generate_choices(
                    story_data['content'],
                    current_emotion,
                    target_emotion
                )
            
            return story_data
            
        except Exception as e:
            print(f"Error generating story: {str(e)}")
            return self._get_fallback_story(story_type, current_emotion)
    
    def _build_story_prompt(self, story_type, current_emotion, intensity,
                           target_emotion, theme, preferences, min_words, max_words):
        """Build detailed prompt for story generation"""
        
        prompt = f"""
        Create a {story_type} story with the following specifications:
        
        EMOTIONAL CONTEXT:
        - Current emotion: {current_emotion} (intensity: {intensity}/10)
        - Target emotion: {target_emotion or 'balanced and peaceful'}
        - Theme: {theme}
        
        STORY REQUIREMENTS:
        - Length: {min_words}-{max_words} words
        - Type: {story_type}
        - Style: Immersive, therapeutic, and emotionally resonant
        """
        
        if preferences:
            prompt += f"\n\nUSER PREFERENCES:\n"
            for key, value in preferences.items():
                prompt += f"- {key}: {value}\n"
        
        prompt += f"""
        
        STRUCTURE:
        Please provide the story in JSON format with:
        1. "title": An evocative title
        2. "content": The main story text divided into chapters
        3. "chapters": Array of chapter objects with "number", "title", and "text"
        4. "emotional_arc": Array describing the emotional journey
        5. "key_moments": Array of transformative moments in the story
        6. "reflection_prompts": Questions for the reader to consider
        
        For interactive stories, also include:
        7. "choices": Array of decision points with options and consequences
        8. "branches": Different story paths based on choices
        
        THERAPEUTIC ELEMENTS:
        - Start by acknowledging the current emotion
        - Gradually introduce elements that shift toward the target emotion
        - Include metaphors that resonate with the emotional journey
        - End with a sense of resolution or new perspective
        
        Make the story engaging, meaningful, and helpful for emotional processing.
        """
        
        return prompt
    
    def _generate_choices(self, story_content: str, current_emotion: str, 
                         target_emotion: Optional[str]) -> List[Dict]:
        """Generate interactive choices for the story"""
        
        choices = []
        
        # Create 3 decision points
        for i in range(3):
            choice = {
                'id': f'choice_{i+1}',
                'chapter': i + 2,
                'prompt': f'What would you like to do?',
                'options': [
                    {
                        'id': f'option_{i+1}_a',
                        'text': f'Take the path of {random.choice(["courage", "wisdom", "compassion"])}',
                        'emotional_impact': {
                            current_emotion: -1,
                            target_emotion or 'peace': +1
                        },
                        'next_chapter': i + 3
                    },
                    {
                        'id': f'option_{i+1}_b',
                        'text': f'Choose the way of {random.choice(["patience", "acceptance", "action"])}',
                        'emotional_impact': {
                            current_emotion: -2,
                            target_emotion or 'balance': +2
                        },
                        'next_chapter': i + 3
                    }
                ]
            }
            choices.append(choice)
        
        return choices
    
    def continue_story(self, story_id: str, choice_id: str, 
                      story_context: Dict) -> Dict:
        """
        Continue an interactive story based on user choice
        
        Args:
            story_id: ID of the current story
            choice_id: ID of the choice made
            story_context: Current story state and history
        
        Returns:
            Dictionary with next chapter content
        """
        
        prompt = f"""
        Continue this interactive story based on the user's choice:
        
        STORY CONTEXT:
        Current chapter: {story_context.get('current_chapter', 1)}
        Choices made so far: {story_context.get('choices_made', [])}
        Selected choice: {choice_id}
        
        Previous content summary: {story_context.get('summary', '')}
        
        Generate the next chapter (300-500 words) that:
        1. Naturally flows from the choice made
        2. Advances the emotional journey
        3. Introduces new elements or revelations
        4. Maintains narrative coherence
        
        Return as JSON with:
        - "chapter_number": int
        - "chapter_title": string
        - "content": string
        - "choices": array of new choices (if applicable)
        - "emotional_tone": string
        - "key_development": string
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are continuing an interactive therapeutic story. Maintain consistency while advancing the narrative based on user choices."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=1000
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error continuing story: {str(e)}")
            return {
                'chapter_number': story_context.get('current_chapter', 1) + 1,
                'content': 'The story continues on your chosen path...',
                'emotional_tone': 'neutral'
            }
    
    def _get_fallback_story(self, story_type: str, emotion: str) -> Dict:
        """Return a fallback story if generation fails"""
        
        fallback_stories = {
            'healing': {
                'title': 'The Garden of Renewal',
                'content': 'In a quiet corner of the world, there exists a garden where emotions bloom like flowers...',
                'chapters': [
                    {
                        'number': 1,
                        'title': 'The Entrance',
                        'text': 'You stand before an ancient gate, weathered by time but still standing strong...'
                    }
                ],
                'emotional_arc': ['acknowledgment', 'exploration', 'acceptance', 'growth'],
                'reading_time': 5
            },
            'adventure': {
                'title': 'The Journey Within',
                'content': 'Every adventure begins with a single step, and yours begins now...',
                'chapters': [
                    {
                        'number': 1,
                        'title': 'The Call',
                        'text': 'The morning sun reveals a path you\'ve never noticed before...'
                    }
                ],
                'emotional_arc': ['curiosity', 'challenge', 'discovery', 'triumph'],
                'reading_time': 7
            }
        }
        
        return fallback_stories.get(story_type, fallback_stories['healing'])