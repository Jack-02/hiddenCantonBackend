from django.shortcuts import render
from django.http import JsonResponse
import json

# Create your views here.
def index(req):
    body = json.loads(req.body.decode("utf-8"))
    return JsonResponse({"request": body["id"]})