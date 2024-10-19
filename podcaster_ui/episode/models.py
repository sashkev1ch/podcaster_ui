from django.db import models
# local
from podcaster_ui.channel.models import Channel


class CustomDateTimeField(models.DateTimeField):
    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val:
            return val.strftime("%Y-%m-%d %H:%M:%S")
        return ''


class Episode(models.Model):
    title = models.CharField(max_length=200, null=False)
    # pub_date = CustomDateTimeField(null=False)
    pub_date = models.DateTimeField(null=False)
    external_guid = models.CharField(max_length=60, null=False, unique=True)
    description = models.TextField()
    url = models.CharField(max_length=200, null=False)
    added = models.DateTimeField(auto_now=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=False)
