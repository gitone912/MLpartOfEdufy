# yt_notes_api/views.py

import json
import os
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ProcessedNote
from .serializers import ProcessedNoteSerializer
from pytube import YouTube
import subprocess
import whisper
import pandas as pd
from django.conf import settings
import random
# from transformers import AutoTokenizer, AutoModelWithLMHead
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
def process_youtube_link(request):
    randomNum = random.randint(0, 100000000)
    if request.method == 'POST':
        youtube_link = request.data.get('youtube_link')
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_files')

        try:
            # Download the YouTube video
            download_youtube_video(youtube_link, save_path)

            # Extract audio from the video
            input_video_path = f"{save_path}/video.mp4"
            output_audio_path = f"{save_path}/newaudi{randomNum}o.wav"
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
        

# def getsummary(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             text = data.get('text')
#             summary = get_summary(text)
#             return JsonResponse({'summary': summary})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
# @csrf_exempt
# def solveqna(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             text = data.get('text')
#             question = data.get('question')
#             answer = get_qna(text, question)
#             return JsonResponse({'answer': answer})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)


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

# def get_summary(text):
#     # Load the model
#     model = AutoModelWithLMHead.from_pretrained("t5-base")
#     tokenizer = AutoTokenizer.from_pretrained("t5-base")

#     # Tokenize the text
#     inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)

#     # Generate the summary
#     outputs = model.generate(
#         inputs, 
#         max_length=150, 
#         min_length=40, 
#         length_penalty=2.0, 
#         num_beams=4, 
#         early_stopping=True
#     )

#     # Decode the summary
#     summary = tokenizer.decode(outputs[0])

#     return summary

# def get_qna(text,question):
#     model_name = "MaRiOrOsSi/t5-base-finetuned-question-answering"
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelWithLMHead.from_pretrained(model_name)
#     input = f"question: {question} context: {text}"
#     encoded_input = tokenizer([input],
#                              return_tensors='pt',
#                              max_length=512,
#                              truncation=True)
#     output = model.generate(input_ids = encoded_input.input_ids,
#                             attention_mask = encoded_input.attention_mask)
#     output = tokenizer.decode(output[0], skip_special_tokens=True)
#     return output