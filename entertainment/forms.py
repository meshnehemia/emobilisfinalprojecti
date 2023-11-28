# forms.py
from django import forms
from .models import MyVideos


class VideoForm(forms.ModelForm):
    class Meta:
        model = MyVideos
        fields = ['video_title', 'video_description', 'video_image', 'video', 'type','cost']
