from datetime import datetime
from typing import Optional, Dict, List, Union, Any
from requests import get
from rss_parser import RSSParser
from dateutil.parser import parse
from re import search

# local
from podcaster_ui.channel.models import Channel
from podcaster_ui.utils.constants import TIMEZONE_INFO


class RssParseException(Exception): ...


def get_tz_info(date_string: str) -> Optional[Dict[str, int]]:
    possible_tzs = list(TIMEZONE_INFO.keys())
    for tz_name in possible_tzs:
        position = date_string.find(tz_name)
        if position > 0:
            if search("[A-Z]", date_string[position + len(tz_name) :]):
                continue
            return {tz_name: TIMEZONE_INFO[tz_name]}

    return None


def get_datetime(date_string: str) -> datetime:
    tz_info = get_tz_info(date_string)
    return parse(date_string, tzinfos=tz_info)


def get_content(obj, attr: str = "content") -> Union[str, datetime, int, None]:
    try:
        content = getattr(obj, attr)
    except AttributeError:
        content = None

    return content


def get_rss_channel(url: str) -> Dict[str, Any]:
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


def get_rss_data(
    channel: Channel,
) -> List[Dict[str, Union[str, int, datetime, Channel, None]]]:
    response = get(channel.url)
    if response.status_code != 200:
        raise RssParseException(
            f"Can't reach rss url {channel.url}, returned status code: {response.status_code}"
        )
    rss = RSSParser.parse(response.text)

    episodes = []
    for item in rss.channel.items:
        try:
            episode_url = item.enclosures[0].attributes.get("url", "")
        except (IndexError, AttributeError):
            episode_url = ""

        episodes.append(
            {
                "title": get_content(item.title),
                "external_guid": get_content(item.guid),
                "pub_date": get_datetime(get_content(item.pub_date)),
                "description": get_content(item.description),
                "url": episode_url,
                "channel": channel,
            }
        )
        episodes = sorted(episodes, key=lambda d: d["pub_date"], reverse=True)

    return episodes
