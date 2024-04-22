import json
from django.shortcuts import render
from django.http import HttpRequest
from django.utils import timezone
from django.db import IntegrityError
from spot.models import Spot, Route, Video, Audio, SpotInRoute
from spot.utils import check_spot
from utils.utils_require import CheckRequire, require
from utils.utils_request import (
    NO_PERMISSION,
    BAD_METHOD,
    request_failed,
    request_success,
    return_field,
)
from user.utils import req_identity

# Create your views here.


@CheckRequire
def info(req: HttpRequest):
    identity = req_identity(req)
    if req.method == "GET":
        page = require(req.GET, "page", "int")
        num_per_page = require(req.GET, "num_per_page", "int")
        if "name" in req.GET.keys():
            spots = Spot.objects.get(name=req.GET["name"])
            return_data = {
                "total_records": spots.count(),
                "spots": [spot.serialise(True) for spot in spots[(page - 1) * num_per_page:page * num_per_page]]
            }
            return request_success(return_data)
        else:
            spots = Spot.objects.all()
            return_data = {
                "total_records": spots.count(),
                "spots": [spot.serialise(True) for spot in spots[(page - 1) * num_per_page:page * num_per_page]]
            }
            return request_success(return_data)
    elif req.method == "PUT":
        body = json.loads(req.body.decode("utf-8"))
        if identity < 2:
            return NO_PERMISSION
        name, location, text, quote, video_titles, video_cloudids, audio_titles, audio_cloudids = check_spot(
            body)
        spot = Spot.objects.create(
            name=name, location=location, text=text, quote=quote)
        for title, cloudid in zip(video_titles, video_cloudids):
            Video.objects.create(title=title, cloudid=cloudid, spot=spot)
        for title, cloudid in zip(audio_titles, audio_cloudids):
            Audio.objects.create(title=title, cloudid=cloudid, spot=spot)
        return request_success({"id": spot.id})
    elif req.method == "DELETE":
        body = json.loads(req.body.decode("utf-8"))
        if identity < 2:
            return NO_PERMISSION
        id = require(body, "id", "int")
        try:
            spot = Spot.objects.get(id=id)
            spot.delete()
        except Spot.DoesNotExist:
            return request_failed(1, "Spot Does Not Exist")
        except IntegrityError:
            return request_failed(2, "Spot Included In Route")
        return request_success()
    elif req.method == "POST":
        body = json.loads(req.body.decode("utf-8"))
        if identity < 2:
            return NO_PERMISSION
        id = require(body, "id", "int")
        name, location, text, quote, video_titles, video_cloudids, audio_titles, audio_cloudids = check_spot(
            body)
        try:
            spot = Spot.objects.get(id=id)
        except Spot.DoesNotExist:
            return request_failed(1, "Spot Does Not Exist")
        spot.name = spot.name
        spot.location = location
        spot.text = text
        spot.quote = quote
        for video in Video.objects.filter(spot=spot):
            video.delete()
        for audio in Audio.objects.filter(spot=spot):
            audio.delete()
        spot.save()
        for title, cloudid in zip(video_titles, video_cloudids):
            Video.objects.create(title=title, cloudid=cloudid, spot=spot)
        for title, cloudid in zip(audio_titles, audio_cloudids):
            Audio.objects.create(title=title, cloudid=cloudid, spot=spot)
        return request_success()
    else:
        return BAD_METHOD


@CheckRequire
def route(req: HttpRequest):
    pass
