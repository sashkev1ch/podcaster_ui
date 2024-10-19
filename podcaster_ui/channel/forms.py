from django.forms import ModelForm
# local
from podcaster_ui.channel.models import Channel


class ChannelForm(ModelForm):
    class Meta:
        model = Channel
        fields = ["name", "url", "description"]
