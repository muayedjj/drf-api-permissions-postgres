from django.db import models
from django.conf import settings


class Book(models.Model):
    title = models.CharField(max_length=256)
    synopsis = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Post(models.Model):
    anything = models.CharField(max_length=256)

    def __str__(self):
        return self.anything
