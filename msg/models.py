from django.db import models
from django.utils import timezone
from user.models import User
from spot.models import Spot

# Create your models here.


class Message(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)

    def serialise(self):
        return {
            "id": self.id,
            "user": self.user.openid,
            "title": self.title,
            "spots": [info.spot.serialise(verbose=False) for info in SpotInMessage.objects.filter(message=self)],
            "text": self.text,
            "image": [image.cloudid for image in Image.objects.filter(message=self)],
            "video": [video.cloudid for video in Video.objects.filter(message=self)],
            "time": self.time
        }


class SpotInMessage(models.Model):
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE)
    spot = models.ForeignKey(to=Spot, on_delete=models.CASCADE)


class Image(models.Model):
    cloudid = models.CharField(max_length=50)
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE)


class Video(models.Model):
    cloudid = models.CharField(max_length=50)
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE)
