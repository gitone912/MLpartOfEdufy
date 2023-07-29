# yt_notes_api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('process_youtube_link/', views.process_youtube_link, name='process_youtube_link'),
]
