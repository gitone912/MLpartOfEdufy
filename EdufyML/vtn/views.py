# yt_notes_api/views.py

import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ProcessedNote
from .serializers import ProcessedNoteSerializer
from pytube import YouTube
import subprocess
import whisper
import pandas as pd
from django.conf import settings
@api_view(['POST'])
def process_youtube_link(request):
    if request.method == 'POST':
        youtube_link = request.data.get('youtube_link')
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_files')

        try:
            # Download the YouTube video
            download_youtube_video(youtube_link, save_path)

            # Extract audio from the video
            input_video_path = f"{save_path}/video.mp4"
            output_audio_path = f"{save_path}/newaudio.wav"
            extract_audio(input_video_path, output_audio_path)

            # Use Whisper AI model to transcribe audio and get notes
            model = whisper.load_model("tiny")
            result = model.transcribe(output_audio_path)

            # Save the transcribed notes to a file
            with open(f'{save_path}/whisperai.txt', 'w') as f:
                f.write(result['text'])

            # Prepare the notes text to store in the database
            notes_text = result['text']

            # Save the processed notes in the database
            processed_note = ProcessedNote.objects.create(youtube_link=youtube_link, notes_text=notes_text)
            serializer = ProcessedNoteSerializer(processed_note)

            return Response(serializer.data)

        except Exception as e:
            return Response({'error': str(e)}, status=400)

def download_youtube_video(link, save_path):
    try:
        # Object creation using YouTube
        yt = YouTube(link)
    except:
        raise Exception("Connection Error")  # To handle exceptions

    # Get the highest resolution stream (usually mp4)
    d_video = yt.streams.get_highest_resolution()

    try:
        # Downloading the video
        d_video.download(save_path, filename="video.mp4")
    except:
        raise Exception("Some Error!")

    print('Task Completed!')

def extract_audio(input_path, output_path):
    command = ['ffmpeg', '-i', input_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', output_path]
    try:
        subprocess.run(command, check=True)
        print("Audio extraction successful!")
    except subprocess.CalledProcessError as e:
        raise Exception("Error occurred:", e)
