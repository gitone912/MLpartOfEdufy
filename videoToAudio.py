import subprocess

def extract_audio(input_path, output_path):
    command = ['ffmpeg', '-i', input_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', output_path]
    try:
        subprocess.run(command, check=True)
        print("Audio extraction successful!")
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)

# input_video_path = "gfg.mp4"
input_video_path = "cheatsheet.mp4"
output_audio_path = "/Users/pranaymishra/Desktop/MLpartOfEdufy/cheatsheet.wav"

extract_audio(input_video_path, output_audio_path)
