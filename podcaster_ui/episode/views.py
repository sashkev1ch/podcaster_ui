from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

# local
from podcaster_ui.episode.models import Episode
from podcaster_ui.channel.models import Channel
from podcaster_ui.celery import download


class EpisodeView(View):
    def get(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel, id=kwargs.get("channel_id"))
        episode = get_object_or_404(Episode, id=kwargs.get("episode_id")).order_by("-pub_date")
        return render(request, "episode/index.html", context={"episode": episode, "channel_name": channel.name})


class DownloadEpisodeView(View):
    def get(self, request, *args, **kwargs):
        episode = get_object_or_404(Episode, id=kwargs.get("episode_id"))
        channel = get_object_or_404(Channel, id=kwargs.get("channel_id"))
        t = download.delay(url=episode.url, title=episode.title, channel_name=channel.name)
        return redirect("view_channel", channel_id=kwargs.get("channel_id"))
