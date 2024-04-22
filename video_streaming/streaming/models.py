from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Video(models.Model):
    name = models.CharField(max_length=200)
    video_url = models.FileField(upload_to="videos")
    userid = models.ForeignKey(User,on_delete = models.CASCADE,related_name = "videos")

    def __str__(self):
        return self.name