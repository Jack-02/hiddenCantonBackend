from django.db import models

# Create your models here.
class User(models.Model):
    phone = models.IntegerField()
    last_login = models.DateTimeField()