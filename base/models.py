from django.db import models

# Create your models here.

class AudioResource(models.Model):
    audio=models.FileField(upload_to="uploads")
    was_saved=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    thumbnail_url=models.CharField(max_length=100,blank=True,null=True)
    video_title=models.CharField(max_length=200,blank=True,null=True)
    video_size=models.CharField(max_length=50,null=True,blank=True)
    
