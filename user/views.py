import json
from django.shortcuts import render
from django.http import HttpRequest
from django.utils import timezone
from user.models import User
from utils.utils_require import CheckRequire, require
from utils.utils_request import (
    BAD_METHOD,
    request_failed,
    request_success,
    return_field,
)


# Create your views here.
@CheckRequire
def user(req: HttpRequest):
    if req.method == "PUT":
        body = json.loads(req.body.decode("utf-8"))
        phone = require(body, "phone", "int", "Missing or error type of [phone]")
        user = User(phone=phone, create_time=timezone.now())
        user.save()
        return request_success()
    elif req.method == "GET":
        users = User.objects.all()
        return_data = {
            "users": [
                {"phone": user.phone, "create_time": user.create_time} for user in users
            ]
        }
        return request_success(return_data)
    else:
        return BAD_METHOD
