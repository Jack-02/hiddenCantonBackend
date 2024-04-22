import json
from django.db import models

# Create your models here.


class Spot(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    text = models.TextField()
    quote = models.TextField()

    def serialise(self, verbose):
        if verbose:
            return {
                "id": self.id,
                "name": self.name,
                "location": self.location,
                "info": {
                    "text": self.text,
                    "quote": self.quote,
                    "video": [video.serialise() for video in Video.objects.filter(spot_id=self.id)],
                    "audio": [audio.serialise() for audio in Audio.objects.filter(spot_id=self.id)]
                }
            }
        else:
            return {
                "id": self.id,
                "name": self.name,
            }


class Video(models.Model):
    cloudid = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=50)
    spot = models.ForeignKey(to=Spot, on_delete=models.CASCADE)

    def serialise(self):
        return {
            "cloudid": self.cloudid,
            "title": self.title
        }


class Audio(models.Model):
    cloudid = models.CharField(max_length=50, primary_key=True)
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
            "spots": [spot.serialise(False) for spot in json.loads(self.spots)]
        }

class SpotInRoute(models.Model):
    spot = models.ForeignKey(Spot, models.PROTECT)
    route = models.ForeignKey(Route, models.CASCADE)