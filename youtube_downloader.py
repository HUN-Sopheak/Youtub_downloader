from pytube import YouTube
import os
import time
from tqdm import tqdm

def show_progress_bar(stream, chunk, bytes_remaining):
    current = ((stream.filesize - bytes_remaining) / stream.filesize)
    percent = ('{0:.1f}').format(current * 100)
    progress = int(50 * current)
    status = '█' * progress + '-' * (50 - progress)
    print(f'\r|{status}| {percent}%', end='')

def download_video(url):
    try:
        yt = YouTube(url)
        yt.register_on_progress_callback(show_progress_bar)
        
        stream = yt.streams.get_highest_resolution()
        output_dir = os.path.join(os.getcwd(), 'video')  # Cross-platform directory path
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created new directory: {output_dir}")
        
        title = yt.title
        forbidden_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in forbidden_characters:
            title = title.replace(char, '')
        
        custom_filename = f"{title}.mp4"
        output_path = os.path.join(output_dir, custom_filename)  # Cross-platform file path
        if os.path.exists(output_path):
            print("File already exists.")
            return None
        
        stream.download(output_path=output_path)
        print(f"\nVideo downloaded successfully: {output_path}")
        
        # Cross-platform way to handle file permissions
        if os.name == 'nt':  # If the OS is Windows
            os.chmod(output_path, 0o666)  # Sets the file to be readable and writable by all users
        else:
            os.chmod(output_path, 0o644)  # Sets the file to be readable and writable by the owner, and readable by others
        
        return output_path  
    except Exception as e:
        print(f"\nError downloading video: {str(e)}")
        return None

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    video_file = download_video(video_url)
    if not video_file:
        print("Failed to download the video.")
