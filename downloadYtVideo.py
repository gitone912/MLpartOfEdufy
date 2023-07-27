from pytube import YouTube

def download_youtube_video(link, save_path):
    try:
        # Object creation using YouTube
        yt = YouTube(link)
    except:
        print("Connection Error")  # To handle exceptions

    # Get the highest resolution stream (usually mp4)
    d_video = yt.streams.get_highest_resolution()

    try:
        # Downloading the video
        d_video.download(save_path)
    except:
        print("Some Error!")
    print('Task Completed!')

# Example usage:
# video_link = "https://www.youtube.com/watch?v=xWOoBJUqlbI"
video_link = "https://youtu.be/M0JIy8sMN4A"
SAVE_PATH = "/Users/pranaymishra/Desktop/MLpartOfEdufy"
download_youtube_video(video_link, SAVE_PATH)
