import json
from django.shortcuts import render
from django.http import HttpRequest
from django.utils import timezone
from user.models import User
from utils.utils_require import CheckRequire, require
from utils.utils_request import (
    NO_PERMISSION,
    BAD_METHOD,
    request_failed,
    request_success,
    return_field,
)
from user.utils import req_identity, req_openid


# Create your views here.
@CheckRequire
def user(req: HttpRequest):
    if req_identity(req) != 2:
        return NO_PERMISSION
    if req.method == "GET":
        page = require(req.GET, "page", "int")
        num_per_page = require(req.GET, "num_per_page", "int")
        return_data = {
            "total_records": User.objects.count(),
            "users": [return_field(user.serialise(), ["openid", "identity"])
                      for user in User.objects.all()[(page - 1) * num_per_page:page * num_per_page]]
        }
        return request_success(return_data)
    elif req.method == "POST":
        body = json.loads(req.body.decode("utf-8"))
        page = require(body, "page", "int")
        num_per_page = require(body, "num_per_page", "int")
        result = User.objects.all()
        if "openid" in body.keys():
            result = result.filter(openid=body["openid"])
        if "identity" in body.keys():
            result = result.filter(openid=body["identity"])
        return_data = {
            "total_records": result.count(),
            "users": [return_field(user.serialise(), ["openid", "identity"])
                      for user in list(result[(page - 1) * num_per_page:page * num_per_page])]
        }
        return request_success(return_data)
    else:
        return BAD_METHOD

@CheckRequire
def user_id(req: HttpRequest):
    if req.method == "POST":
        if req_identity(req) != 2:
            return NO_PERMISSION
        body = json.loads(req.body.decode("utf-8"))
        identity = require(body, "identity", "int")
        openid = require(body, "openid", "string")
        if openid == req_openid(req):
            return request_failed(3, "Modifying Oneself")
        if identity > 1 or identity < 0:
            return request_failed(2, "Wrong Identity")
        try: 
            user = User.objects.get(openid=openid)
            user.identity = identity
            user.save()
        except:
            return request_failed(1, "User does not exist")
        return request_success()
    else:
        return BAD_METHOD
