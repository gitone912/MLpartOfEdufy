# yt_notes_api/serializers.py

from rest_framework import serializers
from .models import ProcessedNote

class ProcessedNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedNote
        fields = ['id', 'youtube_link', 'notes_text', 'created_at']
