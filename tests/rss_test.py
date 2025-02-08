from typing import Union
from datetime import datetime
from requests import get
from rss_parser import RSSParser
# from pprint import pprint
# local

# channel_url = "http://feeds.rucast.net/radio-t"
channel_url = "https://softskills.audio/feed.xml"


class RssParseException(Exception): ...


def get_content(obj, attr: str = "content") -> Union[str, datetime, int, None]:
    try:
        content = getattr(obj, attr)
    except AttributeError:
        content = None

    return content


def get_rss_channel(url: str):
    response = get(url)
    if response.status_code != 200:
        raise RssParseException(
            f"Can't reach rss url {url}, returned status code: {response.status_code}"
        )
    rss = RSSParser.parse(response.text)

    channel = {
        "name": get_content(rss.channel.title),
        "description": get_content(rss.channel.description),
    }

    return channel


get_rss_channel(channel_url)
