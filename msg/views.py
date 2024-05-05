import json
from django.shortcuts import render
from django.http import HttpRequest
from django.db import IntegrityError
from utils.utils_require import CheckRequire, require
from utils.utils_request import (
    NO_PERMISSION,
    BAD_METHOD,
    request_failed,
    request_success
)
from user.utils import req_identity, req_openid
from msg.models import Message, Image, Video, SpotInMessage
from spot.models import Spot
from user.models import User

# Create your views here.


@CheckRequire
def msg(req: HttpRequest):
    identity = req_identity(req)
    if req.method == "GET":
        page = require(req.GET, "page", "int")
        num_per_page = require(req.GET, "num_per_page", "int")
        msgs = Message.objects.all()
        return_data = {
            "total_records": msgs.count(),
            "messages": [message.serialise() for message in msgs[(page - 1) * num_per_page:page * num_per_page]]
        }
        return request_success(return_data)
    elif req.method == "PUT":
        body = json.loads(req.body.decode("utf-8"))
        title = require(body, "title", "string")
        spots = require(body, "spots", "list")
        text = require(body, "text", "string")
        image = require(body, "image", "list")
        video = require(body, "video", "list")
        spot_objects = []
        for spot_id in spots:
            try:
                spot_object = Spot.objects.get(id=spot_id)
                spot_objects.append(spot_object)
            except:
                return request_failed(1, "Spot Does Not Exist")
        msg = Message.objects.create(
            title=title, text=text, user=User.objects.get(openid=req_openid(req)))
        for image_id in image:
            Image.objects.create(cloudid=image_id, message=msg)
        for video_id in video:
            Video.objects.create(cloudid=video_id, message=msg)
        for spot_object in spot_objects:
            SpotInMessage.objects.create(spot=spot_object, message=msg)
        return request_success({"id": msg.id})
    elif req.method == "DELETE":
        body = json.loads(req.body.decode("utf-8"))
        id = require(body, "id", "int")
        try:
            message = Message.objects.get(id=id)
        except:
            return request_failed(1, "Message Does Not Exist")
        if identity < 2 and message.user != req_openid(req):
            return NO_PERMISSION
        message.delete()
        return request_success()
    elif req.method == "POST":
        body = json.loads(req.body.decode("utf-8"))
        page = require(req.GET, "page", "int")
        num_per_page = require(req.GET, "num_per_page", "int")
        messages = Message.objects.all()
        if "user" in body.keys():
            messages = messages.filter(user=body["user"])
        if "title" in body.keys():
            messages = messages.filter(title__contains=body["title"])
        return_data = {
            "total_records": messages.count(),
            "messages": [message.serialise() for message in messages[(page - 1) * num_per_page:page * num_per_page]]
        }
        return request_success(return_data)
    else:
        return BAD_METHOD
