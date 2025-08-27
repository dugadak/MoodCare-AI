from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Count, Q
import json

from .models import Story, StoryInteraction, StoryTemplate
from .serializers import (
    StorySerializer,
    StoryCreateRequestSerializer,
    StoryInteractionSerializer,
    StoryChoiceSerializer,
    StoryGenerationResponseSerializer,
    StoryTemplateSerializer,
    StoryProgressSerializer
)
from .ai_generator import StoryGenerator
from emotions.models import Emotion


class StoryViewSet(viewsets.ModelViewSet):
    """ViewSet for interactive AI-generated stories"""
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get user's stories"""
        queryset = Story.objects.filter(user=self.request.user)
        
        # Filter by story type
        story_type = self.request.query_params.get('type')
        if story_type:
            queryset = queryset.filter(story_type=story_type)
        
        # Filter by completion status
        is_completed = self.request.query_params.get('completed')
        if is_completed is not None:
            queryset = queryset.filter(is_completed=is_completed.lower() == 'true')
        
        return queryset.order_by('-last_read_at', '-created_at')
    
    @action(detail=False, methods=['post'], url_path='generate')
    def generate(self, request):
        """Generate a new AI story based on emotional context"""
        serializer = StoryCreateRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Get user's current emotional state
            recent_emotion = Emotion.objects.filter(
                user=request.user
            ).order_by('-created_at').first()
            
            emotion_context = {}
            if recent_emotion:
                emotion_context = {
                    'emotion': recent_emotion.emotion_type,
                    'intensity': recent_emotion.intensity,
                    'triggers': recent_emotion.triggers or [],
                    'context': {
                        'location': recent_emotion.location,
                        'activity': recent_emotion.activity,
                        'weather': recent_emotion.weather
                    }
                }
            
            # Initialize story generator
            generator = StoryGenerator()
            
            # Generate story
            story_data = generator.generate_story(
                story_type=data['story_type'],
                current_emotion=data['current_emotion'],
                emotion_intensity=data['emotion_intensity'],
                target_emotion=data.get('target_emotion'),
                preferences=data.get('preferences', {}),
                length=data.get('length', 'medium')
            )
            
            # Create story in database
            story = Story.objects.create(
                user=request.user,
                title=story_data.get('title', 'Untitled Story'),
                content=story_data.get('content', ''),
                story_type=data['story_type'],
                emotion_context=emotion_context,
                emotion_tags=[
                    data['current_emotion'],
                    data.get('target_emotion', 'balanced')
                ],
                reading_time=story_data.get('reading_time', 5),
                story_branches=story_data.get('branches', {}),
                last_read_at=timezone.now()
            )
            
            # Prepare response
            response_data = {
                'story_id': story.id,
                'title': story.title,
                'first_chapter': story_data.get('chapters', [{}])[0].get('text', story.content[:500]),
                'choices': story_data.get('choices', []),
                'estimated_reading_time': story.reading_time,
                'emotion_journey': story_data.get('emotional_arc', [])
            }
            
            response_serializer = StoryGenerationResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(
                    response_serializer.validated_data,
                    status=status.HTTP_201_CREATED
                )
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='continue')
    def continue_story(self, request, pk=None):
        """Continue an interactive story based on user choice"""
        story = self.get_object()
        choice_id = request.data.get('choice_id')
        
        if not choice_id:
            return Response(
                {'error': 'choice_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Record the choice
        story.choices_made.append({
            'chapter': story.current_chapter,
            'choice_id': choice_id,
            'timestamp': timezone.now().isoformat()
        })
        
        # Generate next chapter
        generator = StoryGenerator()
        next_chapter_data = generator.continue_story(
            story_id=str(story.id),
            choice_id=choice_id,
            story_context={
                'current_chapter': story.current_chapter,
                'choices_made': story.choices_made,
                'summary': story.content[:500]  # Brief summary
            }
        )
        
        # Update story
        story.current_chapter = next_chapter_data.get('chapter_number', story.current_chapter + 1)
        
        # Append new chapter to content
        new_chapter_text = next_chapter_data.get('content', '')
        story.content += f"\n\n## Chapter {story.current_chapter}\n\n{new_chapter_text}"
        
        # Update branches if provided
        if 'branches' in next_chapter_data:
            story.story_branches.update(next_chapter_data['branches'])
        
        story.last_read_at = timezone.now()
        story.save()
        
        # Create interaction record
        StoryInteraction.objects.create(
            story=story,
            user=request.user,
            interaction_type='choice',
            chapter=story.current_chapter - 1,
            choice_id=choice_id,
            choice_text=request.data.get('choice_text', '')
        )
        
        return Response({
            'chapter_number': story.current_chapter,
            'chapter_content': new_chapter_text,
            'choices': next_chapter_data.get('choices', []),
            'emotional_tone': next_chapter_data.get('emotional_tone', 'neutral')
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='interact')
    def interact(self, request, pk=None):
        """Record user interaction with story"""
        story = self.get_object()
        serializer = StoryInteractionSerializer(data=request.data)
        
        if serializer.is_valid():
            interaction = serializer.save(
                story=story,
                user=request.user
            )
            
            # Update story last read time
            story.last_read_at = timezone.now()
            story.save()
            
            return Response({
                'message': 'Interaction recorded',
                'interaction_id': interaction.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, pk=None):
        """Mark story as completed"""
        story = self.get_object()
        story.is_completed = True
        story.last_read_at = timezone.now()
        story.save()
        
        # Record completion interaction
        StoryInteraction.objects.create(
            story=story,
            user=request.user,
            interaction_type='completion',
            chapter=story.current_chapter,
            note=request.data.get('reflection', '')
        )
        
        # Generate completion insights
        total_interactions = StoryInteraction.objects.filter(
            story=story,
            user=request.user
        ).count()
        
        emotional_journey = []
        if story.emotion_context:
            emotional_journey.append(story.emotion_context.get('emotion', 'unknown'))
        if story.emotion_tags:
            emotional_journey.extend(story.emotion_tags)
        
        return Response({
            'message': 'Story completed',
            'story_id': story.id,
            'total_chapters': story.current_chapter,
            'total_interactions': total_interactions,
            'emotional_journey': emotional_journey,
            'reading_time': story.reading_time
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='library')
    def library(self, request):
        """Get user's story library with categories"""
        stories = self.get_queryset()
        
        # Categorize stories
        library = {
            'in_progress': [],
            'completed': [],
            'favorites': [],
            'by_type': {}
        }
        
        # In progress stories
        in_progress = stories.filter(is_completed=False).order_by('-last_read_at')[:5]
        library['in_progress'] = StorySerializer(in_progress, many=True).data
        
        # Completed stories
        completed = stories.filter(is_completed=True).order_by('-last_read_at')[:10]
        library['completed'] = StorySerializer(completed, many=True).data
        
        # Stories by type
        for story_type, label in Story.STORY_TYPES:
            type_stories = stories.filter(story_type=story_type)[:5]
            if type_stories:
                library['by_type'][story_type] = StorySerializer(
                    type_stories, many=True
                ).data
        
        # Statistics
        library['statistics'] = {
            'total_stories': stories.count(),
            'completed_count': stories.filter(is_completed=True).count(),
            'in_progress_count': stories.filter(is_completed=False).count(),
            'total_reading_time': sum(s.reading_time for s in stories),
            'favorite_type': self._get_favorite_story_type(stories)
        }
        
        return Response(library, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='progress')
    def progress(self, request, pk=None):
        """Get reading progress for a story"""
        story = self.get_object()
        
        # Get interactions
        interactions = StoryInteraction.objects.filter(
            story=story,
            user=request.user
        ).order_by('created_at')
        
        # Calculate progress
        total_chapters = len(story.story_branches) + 1 if story.story_branches else 5
        completion_percentage = (story.current_chapter / total_chapters) * 100
        
        # Extract emotional arc
        emotional_arc = []
        if story.emotion_context:
            emotional_arc.append(story.emotion_context.get('emotion', 'neutral'))
        
        # Time spent reading (based on interactions)
        time_spent = 0
        if interactions:
            first_interaction = interactions.first()
            last_interaction = interactions.last()
            if first_interaction and last_interaction:
                time_diff = last_interaction.created_at - first_interaction.created_at
                time_spent = int(time_diff.total_seconds() / 60)  # minutes
        
        progress_data = {
            'story_id': story.id,
            'current_chapter': story.current_chapter,
            'total_chapters': total_chapters,
            'completion_percentage': round(completion_percentage, 2),
            'choices_made': story.choices_made,
            'emotional_arc': emotional_arc,
            'time_spent': time_spent
        }
        
        serializer = StoryProgressSerializer(data=progress_data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        
        return Response(progress_data, status=status.HTTP_200_OK)
    
    def _get_favorite_story_type(self, stories):
        """Determine user's favorite story type"""
        type_counts = stories.values('story_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        if type_counts:
            return type_counts[0]['story_type']
        return 'healing'


class StoryTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for story templates"""
    serializer_class = StoryTemplateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get active story templates"""
        queryset = StoryTemplate.objects.filter(is_active=True)
        
        # Filter by story type
        story_type = self.request.query_params.get('type')
        if story_type:
            queryset = queryset.filter(story_type=story_type)
        
        # Filter by target emotion
        emotion = self.request.query_params.get('emotion')
        if emotion:
            queryset = queryset.filter(target_emotions__contains=[emotion])
        
        return queryset.order_by('-success_rate', '-usage_count')
    
    @action(detail=True, methods=['post'], url_path='use')
    def use_template(self, request, pk=None):
        """Use a template to generate a story"""
        template = self.get_object()
        
        # Update usage count
        template.usage_count += 1
        template.save()
        
        # Get user's current emotion
        recent_emotion = Emotion.objects.filter(
            user=request.user
        ).order_by('-created_at').first()
        
        current_emotion = 'neutral'
        emotion_intensity = 5
        
        if recent_emotion:
            current_emotion = recent_emotion.emotion_type
            emotion_intensity = recent_emotion.intensity
        
        # Generate story using template
        generator = StoryGenerator()
        story_data = generator.generate_story(
            story_type=template.story_type,
            current_emotion=current_emotion,
            emotion_intensity=emotion_intensity,
            target_emotion=template.target_emotions[0] if template.target_emotions else None,
            preferences={'template_id': template.id},
            length='medium'
        )
        
        # Create story
        story = Story.objects.create(
            user=request.user,
            title=story_data.get('title', template.name),
            content=story_data.get('content', ''),
            story_type=template.story_type,
            emotion_tags=template.target_emotions,
            reading_time=story_data.get('reading_time', 10),
            story_branches=template.template_structure,
            last_read_at=timezone.now()
        )
        
        return Response({
            'story_id': story.id,
            'template_id': template.id,
            'title': story.title,
            'message': 'Story generated from template successfully'
        }, status=status.HTTP_201_CREATED)