# yt_notes_api/models.py

from django.db import models

class ProcessedNote(models.Model):
    youtube_link = models.URLField(max_length=200)
    notes_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ProcessedNote: {self.youtube_link}"
