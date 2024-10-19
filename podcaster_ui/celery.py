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

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def download(self, *args, **kwargs):
    # print(f"Pressed download button!")
    # print(f'Request: {self.request!r}')
    downloads = os.environ.get("DOWNLOAD_PATH")
    file_path = Path(downloads).joinpath(kwargs.get("title"))
    with urlopen(kwargs.get("url")) as response:
        with open(file_path, "wb") as out_file:
            copyfileobj(response, out_file)
