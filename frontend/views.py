from __future__ import unicode_literals
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from frontend.models import VideoURL, Video, VideoURLForm
from downloader.views import create_filename, get_video_info
import re
from unicodedata import normalize
import os
import youtube_dl
from .logger import MyLogger

def slugger(text, delim='-'):

    result = []

    re_obj = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')
    for word in re_obj.split(text):
        word = normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8')
        word = word.replace('/', '')
        if word:
            result.append(word)

    return delim.join(result)
# Create your views here.

def convert(request):
    if request.method == 'POST':
        form = VideoURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            VideoURL.objects.create(url=url)
            ydl_opts = {
            'format':'m4a',

            'postprocessors':[{
                'key':'FFmpegFixupM4a',
                #'preferredcodec':'m4a',
                #'preferredquality':'192',
            }],
            'default_search':'auto',
            'verbose':'True',
            'logger':MyLogger()

            }
            info = get_video_info(url, ydl_opts)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(url)
            youtube_id = info['id']
            title = info['title']
            audio_filename = create_filename(info['title'])
            Video.objects.create(youtube_id=youtube_id, url=url, title=title,audio_filename=audio_filename,timestamp=datetime.datetime.now())
            #if result == 0:
            return render_to_response('download.html', {"filename":audio_filename})
    else:
        form = VideoURLForm
        return render(request,'home.html', {'form':form})
