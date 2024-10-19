from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=200, unique=True)
    # image = ???
    added = models.DateTimeField(auto_now=True)
