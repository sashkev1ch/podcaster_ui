from datetime import datetime
import os
from pathlib import Path
from urllib.request import urlopen
from shutil import copyfileobj
from celery import shared_task

# local
from podcaster_ui.episode.models import Episode

@shared_task(name="download")
def download(episode_id: int, channel_name: str):
    downloads = os.environ.get("DOWNLOAD_PATH", ".")
    channel_path = Path(downloads).joinpath(channel_name)
    if not channel_path.is_dir():
        channel_path.mkdir(parents=True, exist_ok=True)

    ep = Episode.objects.get(pk=episode_id)
    file_path = channel_path.joinpath(ep.title)
    if not file_path.is_file():
        # update episode data
        ep.file_path = str(file_path)
        ep.download_date = datetime.now()
        ep.save()

        with urlopen(ep.url) as response:
            with open(file_path, "wb") as out_file:
                copyfileobj(response, out_file)
