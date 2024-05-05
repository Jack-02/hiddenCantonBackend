from spot.models import Spot, Route, Video, Audio, SpotInRoute
from django.http import HttpRequest
from utils.utils_require import require


def check_spot(body):
    name = require(body, "name", "string")
    location = require(body, "location", "string")
    info = require(body, "info", "dict")
    text = require(info, "text", "string")
    quote = require(info, "quote", "string")
    image = require(info, "image", "list")
    video = require(info, "video", "list")
    audio = require(info, "audio", "list")
    image_titles = []
    video_titles = []
    audio_titles = []
    image_cloudids = []
    video_cloudids = []
    audio_cloudids = []
    for image_single in image:
        title = require(image_single, "title", "string")
        cloudid = require(image_single, "cloudid", "string")
        image_titles.append(title)
        image_cloudids.append(cloudid)
    for video_single in video:
        title = require(video_single, "title", "string")
        cloudid = require(video_single, "cloudid", "string")
        video_titles.append(title)
        video_cloudids.append(cloudid)
    for audio_single in audio:
        title = require(audio_single, "title", "string")
        cloudid = require(audio_single, "cloudid", "string")
        audio_titles.append(title)
        audio_cloudids.append(cloudid)
    return name, location, text, quote, image_titles, image_cloudids, video_titles, video_cloudids, audio_titles, audio_cloudids
