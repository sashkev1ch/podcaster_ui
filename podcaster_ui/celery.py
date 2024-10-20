import os
from pathlib import Path
from urllib.request import urlopen
from shutil import copyfileobj
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'podcaster_ui.settings')

app = Celery('podcaster_ui', backend='redis://localhost', broker='redis://localhost')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def download(self, *args, **kwargs):
    downloads = os.environ.get("DOWNLOAD_PATH")
    channel_path = Path(downloads).joinpath(kwargs.get("channel_name"))
    if not channel_path.is_dir():
        channel_path.mkdir(parents=True, exist_ok=True)

    file_path = channel_path.joinpath(kwargs.get("title"))
    if not file_path.is_file():
        with urlopen(kwargs.get("url")) as response:
            with open(file_path, "wb") as out_file:
                copyfileobj(response, out_file)
