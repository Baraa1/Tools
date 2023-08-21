from django.shortcuts import render
from pathlib import Path
from pytube import YouTube
#import ffmpeg
#import os
#from django.conf import settings
#from django.http import HttpResponse


# Build paths inside the project like this: BASE_DIR / 'subdir'.
OUTPUT_PATH = f'{Path(__file__).resolve().parent.parent}/media/'

def youtube(request):
    return render(request, 'youtube/youtube.html')

# takes a link from the user then fetch the video details and send them back to the user 
# so they can choose a dash or progressive stream to download 
def get_video(request):
    video_id  = request.GET.get('video_id')
    #if 'session_key' in request.session:
    # Session exists
    # Add the id to session to pass to the next session
    request.session['video_id'] = video_id
    # if there's a video get its details and show it to the user
    try:
        video = YouTube(video_id)
        # Get all formats
        formats = video.streams.filter(progressive=False).order_by('filesize')
        p_formats = video.streams.filter(progressive=True).order_by('filesize')
        video_title = video.title
        video_description = video.description
        thumbnail = video.thumbnail_url
        # List the available video and audio qualities
        available_video_qualities = {}
        available_audio_qualities = {}
        available_p_video_qualities = {}
        for fr in formats:
            # lists all variables and functions
            #print(dir(fr))
            if fr.type == 'video':
                available_video_qualities[f'{fr.resolution}'] = fr.itag
            elif fr.type == 'audio':
                available_audio_qualities[f'{fr.abr}'] = fr.itag
        for fr1 in p_formats:
            if fr1.type == 'video':
                available_p_video_qualities[f'{fr1.resolution}'] = fr1.itag
            elif fr1.type == 'audio':
                available_p_video_qualities[f'{fr1.abr}'] = fr1.itag

        context = {
            'video_id': video_id,
            'thumbnail': thumbnail,
            'video_title': video_title,
            'video_description': video_description,
            'available_video_qualities': available_video_qualities,
            'available_audio_qualities': available_audio_qualities,
            'available_p_video_qualities': available_p_video_qualities,
        }
    except:
        # Default values
        context = {
            'video_id': "video_id",
            'thumbnail': "https://www.google.com/imgres?imgurl=https%3A%2F%2Fwww.youtube.com%2Fimg%2Fdesktop%2Fyt_1200.png&tbnid=rTmhTV_p1VaHyM&vet=12ahUKEwiloZiHlO2AAxUwyLsIHbzGBl4QMygBegQIARBu..i&imgrefurl=https%3A%2F%2Fwww.youtube.com%2Findex%3Fdesktop_uri%3D%252F%26app%3Ddesktop&docid=NU9nCUZVKqM_sM&w=1200&h=1200&q=youtube&ved=2ahUKEwiloZiHlO2AAxUwyLsIHbzGBl4QMygBegQIARBu",
            'video_title': "Title",
            'video_description': "Description",
            'available_video_qualities': " ",
            'available_audio_qualities': " ",
            'available_p_video_qualities': " ",
        }
    print(context)
    return render(request, 'youtube/download_video.html', context)

# a view that serves download links to the end user
def download_links(request):
    # get the id from the session
    video_id = request.session.get('video_id')
    # Get the video
    video = YouTube(video_id)
    formats = video.streams.filter(progressive=False).order_by('filesize')
    p_formats = video.streams.filter(progressive=True).order_by('filesize')

    if request.method == 'POST':
        # Get the selected audio and video quality
        v_quality = request.POST.get('video_quality')
        a_quality = request.POST.get('audio_quality')
        pv_quality = request.POST.get('p_video_quality')

        try:
            video_quality = formats.get_by_itag(v_quality)
            video_link = video_quality.url
            v_quality = video_quality.resolution
        except:
            video_quality = '#'
            video_link = '#'
            v_quality = '#'
        try:
            audio_quality = formats.get_by_itag(a_quality)
            audio_link = audio_quality.url
            a_quality = audio_quality.abr
        except:
            audio_quality = '#'
            audio_link = '#'
            a_quality = '#'
        try:
            p_video_quality = p_formats.get_by_itag(pv_quality)
            p_video_link = p_video_quality.url
            pv_quality = p_video_quality.resolution
        except:
            p_video_quality = '#'
            p_video_link = '#'
            pv_quality = '#'

        filename = video_quality.default_filename
        filename = filename.replace(" ", "-")
        context = {
            "filename":filename,
            "video_link":video_link,
            "audio_link":audio_link,
            "p_video_link":p_video_link,
            "video_quality":video_quality.resolution,
            "audio_quality":a_quality,
            "p_video_quality":pv_quality,
            }
        # Download the video and audio streams
        return render(request, 'youtube/includes/download_links.html', context)

# this is for merging audio and video files but because of the huge size of high quality videos, 
# it takes too much time to download then again too much time to merge it with the audio file
# it proved useless at my current skill level
# will come back to it if I learned a good way to do it
#def download_video(request):
#    # get the id from the session
#    video_id = request.session.get('video_id')
#    # Get the video
#    video = YouTube(video_id)
#    formats = video.streams.filter(progressive=False).order_by('filesize')
#    formats = video.streams.filter(progressive=False).order_by('filesize')
#
#    if request.method == 'POST':
#        # Get the selected audio and video quality
#        v_quality = request.POST.get('video_quality')
#        a_quality = request.POST.get('audio_quality')
#
#        # Get the video and audio qualities from the user
#        video_quality = formats.get_by_itag(v_quality)
#        audio_quality = formats.get_by_itag(a_quality)
#        mime_type = video_quality.mime_type
#
#    
#        filename = video_quality.default_filename
#        filename = filename.replace(" ", "-")
#        # Download the video and audio streams
#        video_quality.download(OUTPUT_PATH, filename = filename)
#        audio_quality.download(OUTPUT_PATH, filename = filename,filename_prefix='audio-')
#        # Select the video and audio streams for ffmpeg
#        video_stream = ffmpeg.input(f'{OUTPUT_PATH}/{filename}')
#        audio_stream = ffmpeg.input(f'{OUTPUT_PATH}/audio-{filename}')
#    
#        # Merge the video and audio streams
#        file_path = f'{OUTPUT_PATH}{filename}.mp4'
#        ffmpeg.output(audio_stream, video_stream, file_path).run()
#        request.session['file_path'] = file_path
#        request.session['filename'] = filename
#        return redirect('serve_file')

#        else:
#            raise Http404

    #return render(request, 'youtube/download_video.html')

# Useful new feature
# ffmpeg.input(url_to_download, ss=FROM, t=TO).output("demo.mp4", vcodec="copy", acodec="copy").overwrite_output().run()

#def serve_file(request):
#    file_path = request.session.get('file_path')
#    filename = request.session.get('filename')
#    #if os.path.exists(file_path):
#    with open(file_path, 'rb') as fh:
#        file_data = fh.read()
#    response = HttpResponse(file_data, content_type='video/mp4')
#    filename = f'{filename}.mp4'
#    response['Content-Disposition'] = 'attachment; filename=' + filename
#    return response
