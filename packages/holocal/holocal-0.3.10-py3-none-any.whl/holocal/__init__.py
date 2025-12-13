import asyncio
from logging import getLogger
from math import ceil
from typing import Dict, Optional, Sequence, Set, Tuple

import aiohttp_client_cache
from aiohttp import ClientTimeout

from holocal.errors import HTTPStatusError
from holocal.schedule import Schedule

CHUNK_SIZE = 50
YOUTUBE_API = "https://www.googleapis.com/youtube/v3/videos"
TARGET = [
    "all",
    "hololive",
    "holostars",
    "indonesia",
    "english",
    "holostars_english",
    "dev_is",
]
log = getLogger(__name__)


class Holocal:
    def __init__(self, page: str,
                 youtube_key: str, save_dir: str) -> None:
        self.page_url = page
        self.yt_key = youtube_key
        self.save_dir = save_dir

        self.session = None
        self.videos: dict = {}

    async def run(self) -> int:
        # ClientSession.__aenter__ does nothing but ClientSession.__aexit__
        # closes this session, so we have to do that.
        # https://github.com/aio-libs/aiohttp/blob/fe647a08d1acb53404b703b46b37409602ab18b4/aiohttp/client.py#L986
        self.session = aiohttp_client_cache.CachedSession(
            cache=aiohttp_client_cache.SQLiteBackend("holocal"),
            timeout=ClientTimeout(
                total=30),
            headers={
                "User-Agent": "holocal"},
        )

        status = 0
        await self.do_run()

        assert self.session
        await self.session.close()

        return status

    async def do_run(self) -> None:
        pages_html = await self.get_pages(TARGET)

        schedules: Dict[str, Schedule] = {}
        for t, p in pages_html.items():
            schedules[t] = Schedule.parse(t, p)

        # currently 'all' has all video ids so fetch this
        video_ids = schedules["all"].video_ids
        await self.get_videos(video_ids)

        for s in schedules.values():
            s.assign_youtube(self.videos)
            log.info(f"Dump {s.name}...")
            s.dump(self.save_dir)

        log.info("Done!")

    async def get_page(self, target: str = "") -> Optional[Tuple[str, str]]:
        log.info(f"({target}) getting page...")

        assert self.session
        async with self.session.get(f"{self.page_url}/{target}") as resp:
            text = await resp.text()
            if resp.status != 200:
                log.error(
                    f"({target}) failed to get: {resp.status} {text}'")
                return None

            return target, text

    async def get_pages(self, targets: Sequence[str]) -> Dict[str, str]:
        pages: Dict[str, str] = {}  # target: content
        tasks = [self.get_page(t) for t in targets]
        res = [r for r in await asyncio.gather(*tasks) if r]
        for r in res:
            target, content = r
            pages[target] = content

        return pages

    async def get_videos(self, video_ids: Set[str]) -> None:
        # divide to chunks each contains 50 videos
        videos = list(video_ids)
        tasks = []
        for i in range(ceil(len(videos) / CHUNK_SIZE)):
            tasks.append(
                self.do_get_videos(
                    videos[i *
                           CHUNK_SIZE: min(len(videos), (i + 1) * CHUNK_SIZE)]
                )
            )

        results = await asyncio.gather(*tasks)
        for resp in results:
            for item in resp["items"]:
                self.videos[item["id"]] = item

    async def do_get_videos(self, video_ids: Sequence[str]) -> dict:
        assert self.session
        async with self.session.get(
                YOUTUBE_API,
                params={
                    "key": self.yt_key,
                    "part": "id,snippet,liveStreamingDetails,contentDetails",
                    "id": ",".join(video_ids),
                },
        ) as resp:
            if resp.status != 200:
                raise HTTPStatusError(resp.status)

            return await resp.json()
