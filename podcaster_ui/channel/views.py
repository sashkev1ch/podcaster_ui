from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models import Max

# local
from podcaster_ui.channel.models import Channel
from podcaster_ui.channel.forms import ChannelForm
from podcaster_ui.episode.models import Episode
from podcaster_ui.utils.tools import get_rss_data, get_rss_channel


class AllChannelsView(View):
    def get(self, request, *args, **kwargs):
        channels = Channel.objects.all()
        return render(request, "channel/index.html", context={"channels": channels})


class ChannelView(View):
    def get(self, request, *args, **kwargs):
        # channel = Channel.objects.get(kwargs["chanel_id"])
        channel = get_object_or_404(Channel, id=kwargs.get("channel_id"))
        episodes = Episode.objects.filter(channel=channel.id).order_by("-pub_date")
        if not episodes:
            episodes = Episode.objects.bulk_create(
                [Episode(**data) for data in get_rss_data(channel)]
            )
        return render(
            request,
            "channel/channel.html",
            context={"channel": channel, "episodes": episodes},
        )


class CreateChannelView(View):
    def get(self, request, *args, **kwargs):
        form = ChannelForm()
        return render(request, "channel/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ChannelForm(request.POST)

        if form.is_valid():
            rss_channel_data = get_rss_channel(request.POST.get("url"))
            channel = form.save(commit=False)

            if not channel.name:
                channel.name = rss_channel_data["name"]
            if not channel.description:
                channel.description = rss_channel_data["description"]

            channel.save()

            episodes = Episode.objects.filter(channel=channel.id)
            if not episodes:
                Episode.objects.bulk_create(
                    [Episode(**data) for data in get_rss_data(channel)]
                )

            channels = Channel.objects.all()

            return render(request, "channel/index.html", context={"channels": channels})


class RefreshChannelView(View):
    def get(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel, id=kwargs.get("channel_id"))
        # db_episodes = Episode.objects.filter(channel=channel.id).order_by("-pub_date")
        last_episode_pub_date = Episode.objects.filter(channel=channel.id).aggregate(
            Max("pub_date", default=date(date.today().year, 1, 1))
        )

        print(f"last episode from db: {last_episode_pub_date}")

        rss_episodes = get_rss_data(channel)
        print(f"last episode from rss: {rss_episodes[0]['pub_date']}")
        Episode.objects.bulk_create(
            [
                Episode(**data)
                for data in rss_episodes
                if data["pub_date"] > last_episode_pub_date["pub_date__max"]
            ]
        )

        channels = Channel.objects.all()
        return render(request, "channel/index.html", context={"channels": channels})


class UpdateChannelView(View):
    def get(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel, id=kwargs.get("channel_id"))
        form = ChannelForm(instance=channel)
        return render(
            request, "channel/update.html", {"form": form, "channel": channel}
        )

    def post(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel, id=kwargs.get("channel_id"))
        form = ChannelForm(request.POST, instance=channel)

        if form.is_valid():
            rss_channel_data = get_rss_channel(request.POST.get("url"))
            channel = form.save(commit=False)

            if not channel.name:
                channel.name = rss_channel_data["name"]
            if not channel.description:
                channel.description = rss_channel_data["description"]

            channel.save()

            episodes = Episode.objects.filter(channel=channel.id)
            if not episodes:
                Episode.objects.bulk_create(
                    [Episode(**data) for data in get_rss_data(channel)]
                )

            channels = Channel.objects.all()

            return render(request, "channel/index.html", context={"channels": channels})

        return render(
            request, "articles/update.html", context={"form": form, "channel": channel}
        )


class DeleteChannelView(View):
    def post(self, request, *args, **kwargs):
        channel = get_object_or_404(Channel, id=kwargs.get("channel_id"))
        channel.delete()

        return redirect("channels")
