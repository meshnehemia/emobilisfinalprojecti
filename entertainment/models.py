from django.db import models

from socialmedia.models import User


# Create your models here.
class MyVideos(models.Model):
    # Your existing fields
    option = (('sale', 'sale'), ('free', 'free'))
    video_title = models.CharField(max_length=50)
    video_description = models.TextField()
    video_image = models.ImageField(upload_to='videocover/')
    video_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=option, default='free')
    cost = models.IntegerField(default=0)
    video = models.FileField(upload_to='uploaded_video/')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_title


class Views(models.Model):
    video = models.ForeignKey(MyVideos, on_delete=models.CASCADE, related_name='video_views')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
