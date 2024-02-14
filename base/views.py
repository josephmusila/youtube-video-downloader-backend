from django.shortcuts import render
from pytube import YouTube
import os
from . import models
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import yt_dlp
# Create your views here.
# pip install yt-dlp
@api_view(['POST'])
def index(request):
    data = request.data

    try:
        youtube_url = data["url"]
        print(youtube_url)
        url = YouTube(str(youtube_url))
        audio_stream = url.streams.filter(only_audio=True).first()

        if audio_stream:
            # Download the audio file
            audio_stream.download()

            # Save the downloaded file path in the model
            audio_item = models.AudioResource.objects.create(audio=audio_stream.title + '.webm')
            print("saved")
            return Response({"download_link": audio_item.audio.url})
        else:
            print("not saved")
            return Response({"download_link": "Not Valid Link"})

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)



@api_view(['POST'])
def index2(request):
    data = request.data

    try:
        youtube_url = data["url"]
        print(youtube_url)
        url = YouTube(str(youtube_url))

        # Get video information
        thumbnail_url = url.thumbnail_url
        video_title = url.title
        video_size = url.streams.filter(only_video=True).first().filesize

        # Download the audio file
        audio_stream = url.streams.filter(only_audio=True).first()
        audio_stream.download()

        # Save the downloaded file path in the model along with video information
        audio_item = models.AudioResource.objects.create(
            audio=audio_stream.title + '.webm',
            thumbnail_url=thumbnail_url,
            video_title=video_title,
            video_size=video_size
        )
        print("saved")
        download_link_absolute = request.build_absolute_uri(audio_item.audio.url)
        response_data = {
            "download_link": download_link_absolute,
            "thumbnail_url": thumbnail_url,
            "video_title": video_title,
            "video_size": video_size
        }

        return Response(response_data)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)
    
    
@api_view(['POST'])
def index3(request):
    data = request.data

    try:
        youtube_url = data["url"]
        print(youtube_url)

        # Use yt_dlp to fetch video details and download the audio in .mp3 format
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)

        # Get information about the downloaded audio
        audio_path = info_dict['title'] + '.mp3'
        thumbnail_url = info_dict.get('thumbnail', '')
        video_title = info_dict.get('title', '')
        video_size = info_dict.get('filesize', 0)

        # Save information in the model
        audio_item = models.AudioResource.objects.create(
            audio=audio_path,
            thumbnail_url=thumbnail_url,
            video_title=video_title,
            video_size=video_size
        )
        print("saved")

        # Build the absolute URL for the download link
        download_link_absolute = request.build_absolute_uri(audio_item.audio.url)

        response_data = {
            "download_link": download_link_absolute,
            "thumbnail_url": audio_item.thumbnail_url,
            "video_title": audio_item.video_title,
            "video_size": audio_item.video_size
        }

        return Response(response_data)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)
    
def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")


def downloader():
    yt = YouTube( 
    str(input("Enter the URL of the video you want to download: \n>> "))) 
  
    # extract only audio 
    video = yt.streams.filter(only_audio=True).first() 
    
    # check for destination to save file 
    print("Enter the destination (leave blank for current directory)") 
    destination = str(input(">> ")) or '.'
    
    # download the file 
    out_file = video.download(output_path=destination) 
    
    # save the file 
    base, ext = os.path.splitext(out_file) 
    new_file = base + '.mp3'
    os.rename(out_file, new_file) 
    
    # result of success 
    print(yt.title + " has been successfully downloaded.")

# link = input("Enter the YouTube video URL: ")
# Download(link)