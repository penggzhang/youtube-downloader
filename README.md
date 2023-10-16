# youtube-downloader
A python script to download Youtube's video, audio and transcript.

Download this Python script into your local folder. Pip install two dependencies: 
- YouTube
- YouTubeTranscriptApi

Run the script to complete the downloading tasks, e.g.

`$ python downloadYoutube.py 'a_youtube_video_url'`

Please use the pair of single quotation marks to enclose the url.

You will be prompted to choose which component shall be downloaded:
1. transcript - both .srt and .txt files
2. video - .mp4 file
3. audio - .webm file
4. all above

Choose what you want, and the code will help you collect the files into the same folder as the script.

The .txt file is a clean-formatted script without timestamps, which is easier for reading.
