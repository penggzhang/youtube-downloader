'''
Usage: 
$ python downloadYoutube.py 'youtube_video_url'

Note: Put youtube's url between single quotation marks.
'''

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import sys

# Callback function for video download progress
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"Already downloaded: {bytes_downloaded} bytes / {total_size} bytes ({percentage:.2f}%)", end='\r')

def download_video(video):
    print('\nDownloading video ...')
    
    video_stream = video.streams.filter(only_video=True, file_extension='mp4', res='1080p').first()
    # If 1080p is unavailable, pick the stream with the highest resolution
    if video_stream is None:
        video_stream = video.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()

    if video_stream:
        print(video_stream)
        video_stream.download()
        print(f'\nSuccessfully downloaded the video file!')
    else:
        print('\nNo video file!')

def download_audio(video):
    print('\nDownloading audio ...')
    video.streams.filter(only_audio=True, file_extension='webm').order_by('abr').desc().first().download()
    print('\nSuccessfully downloaded the audio file!')

def srt_time_format_conversion(srt_time):
    time_formatted = "{:02d}:{:02d}:{:02d},{:03d}".format(
        int(float(srt_time) // 3600),
        int(float(srt_time) // 60 % 60),
        int(float(srt_time) % 60),
        int((float(srt_time) % 1) * 1000)
    )
    return time_formatted

def download_transcript(video):
    print('\nDownloading transcript ...')
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video.video_id)
    except Exception as e:
        print(f"\nTranscript downloading error：{str(e)}")
    else:
        if transcript:
            # Convert transcript into srt and text files
            srt = ""
            txt = ""
            for index, entry in enumerate(transcript):
                start_time = entry['start']
                start_time_formatted = srt_time_format_conversion(start_time)
                if index < len(transcript) - 1:
                    end_time = transcript[index + 1]['start']
                else:
                    end_time = entry['start'] + entry['duration']
                end_time_formatted = srt_time_format_conversion(end_time)
                subtitle = entry['text']

                srt += f"{index + 1}\n"
                srt += f"{start_time_formatted} --> {end_time_formatted}\n"
                srt += f"{subtitle}\n\n"

                txt += f"{subtitle} "

            # Write srt and txt file
            with open(f"{video.title}.srt", "w", encoding="utf-8") as srt_file:
                srt_file.write(srt)

            with open(f"{video.title}.txt", "w", encoding="utf-8") as txt_file:
                txt_file.write(txt)

            print(f"\nSuccessfully downloaded and saved the transcript as {video.title}.srt and {video.title}.txt files.")
        else: 
            print('\nNo subtitle found in this video.')

def view_video_details(video):
    for stream in video.streams:
        print(stream)

def main():
    url = sys.argv[1]

    try:
        my_video = YouTube(url, on_progress_callback=on_progress)
    except VideoUnavailable:
        print(f'\nVideo {url} is unavailable')
    else:
        print(f"\nThe video title is: {my_video.title}")

        user_choice = int(input("""
        Please choose which component you'd like to download from the video:
        1. transcript - both .srt and .txt files
        2. video - .mp4 file
        3. audio - .webm file
        4. all above
        5. just view the video's details instead \n
        """))
        if user_choice == 1:
            download_transcript(my_video)
        elif user_choice == 2:
            download_video(my_video)
        elif user_choice == 3:
            download_audio(my_video)
        elif user_choice == 4:
            download_transcript(my_video)
            download_video(my_video)
            download_audio(my_video)
        elif user_choice == 5:
            view_video_details(my_video)
        else:
            print("\nPlease choose among 1 - 5.")

if __name__ == '__main__':
    main()
