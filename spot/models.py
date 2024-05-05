import json
from django.db import models

# Create your models here.


class Spot(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    text = models.TextField()
    quote = models.TextField()

    def serialise(self, verbose=True):
        if verbose:
            return {
                "id": self.id,
                "name": self.name,
                "location": self.location,
                "info": {
                    "text": self.text,
                    "quote": self.quote,
                    "image": [image.serialise() for image in Image.objects.filter(spot_id=self.id)],
                    "video": [video.serialise() for video in Video.objects.filter(spot_id=self.id)],
                    "audio": [audio.serialise() for audio in Audio.objects.filter(spot_id=self.id)]
                }
            }
        else:
            return {
                "id": self.id,
                "name": self.name,
            }
        
class Image(models.Model):
    cloudid = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    spot = models.ForeignKey(to=Spot, on_delete=models.CASCADE)

    def serialise(self):
        return {
            "cloudid": self.cloudid,
            "title": self.title
        }

class Video(models.Model):
    cloudid = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    spot = models.ForeignKey(to=Spot, on_delete=models.CASCADE)

    def serialise(self):
        return {
            "cloudid": self.cloudid,
            "title": self.title
        }


class Audio(models.Model):
    cloudid = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    spot = models.ForeignKey(to=Spot, on_delete=models.CASCADE)

    def serialise(self):
        return {
            "cloudid": self.cloudid,
            "title": self.title
        }


class Route(models.Model):
    name = models.CharField(max_length=50)
    spots = models.CharField(max_length=100)

    def serialise(self):
        return {
            "id": self.id,
            "name": self.name,
            "spots": [Spot.objects.get(id=spot).serialise(False) for spot in json.loads(self.spots)]
        }

class SpotInRoute(models.Model):
    spot = models.ForeignKey(Spot, models.PROTECT)
    route = models.ForeignKey(Route, models.CASCADE)