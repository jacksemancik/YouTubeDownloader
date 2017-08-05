from django.shortcuts import render

from frontend.models import Video, VideoURL
import youtube_dl


# Create your views here.
def create_filename(value):
    def slugger(text, delim='-'):

        result = []

        re_obj = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')
        for word in re_obj.split(text):
            word = normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8')
            word = word.replace('/', '')
            if word:
                result.append(word)

        return delim.join(result)
    filename = slugger(value, '_')
    if not filename:
        filename = uuid.uuid4
    return '{}.mp3'.format(filename)

def get_video_info(url, ydl_opts):
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    ydl.add_default_info_extractors()
    try:
        return ydl.extract_info(url, download=False)
    except youtube_dl.DownloadError:
        return None
