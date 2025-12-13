import re

from holocal.errors import HolocalException
from holocal.site_type import Type

YOUTUBE_URL = r"https://www[.]youtube[.]com/watch[?]v=(?P<id>[A-Za-z0-9_-]+)"
TWITCH_URL = r"https://www[.]twitch[.]tv/[a-z_]+"


class Site:
    @classmethod
    def parse_url(cls, url: str):
        match = re.search(YOUTUBE_URL, url)
        if match:
            return cls(url, event_id=match["id"])

        elif url == 'https://abema.app/hfAA':
            return cls(url, site_type=Type.Abema)

        elif url == 'https://www.tiktok.com/@houshoumarine_hololivejp':
            return cls(url, site_type=Type.TikTok)

        elif re.match(TWITCH_URL, url):
            return cls(url, site_type=Type.Twitch)

        else:
            raise HolocalException(f"unmatch: {repr(url)}")

    def __init__(self,
                 url: str,
                 site_type: Type = Type.YouTube,
                 event_id: str | None = None):
        self.url: str = url
        self.type: Type = site_type
        self.id: str | None = event_id

    def __repr__(self) -> str:
        return f"<{self.type} {self.id or self.url}>"
