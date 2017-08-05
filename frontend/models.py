from django.db import models
from django.forms import ModelForm

# Create your models here.
class VideoURL(models.Model):
    url = models.URLField(max_length=400)

class VideoURLForm(ModelForm):
    class Meta:
        model = VideoURL
        fields = ['url']

class Video(models.Model):
    youtube_id = models.CharField(max_length=100, unique=True)
    url = models.URLField(max_length=512)
    title = models.TextField()
    duration = models.IntegerField(null=True)
    audio_filename = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.youtube_id
