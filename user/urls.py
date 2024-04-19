from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path("list", views.user),
    path("id", views.user_id)
]
