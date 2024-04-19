from django.db import models


# Create your models here.
class User(models.Model):
    phone = models.IntegerField()
    create_time = models.DateTimeField()
