from user.models import User
from django.http import HttpRequest
from utils.utils_require import require

def req_openid(req: HttpRequest):
    openid = require(req.headers, "x-wx-openid", "string")
    if openid == "":
        raise Exception("No User Info", -5)
    return openid

def req_identity(req: HttpRequest):
    id = require(req.headers, "x-wx-openid", "string")
    if id == "":
        raise Exception("No User Info", -5)
    try:
        user = User.objects.get(openid=id)
        return user.identity
    except:
        user = User(openid=id, identity=0)
        user.save()
        return 0
