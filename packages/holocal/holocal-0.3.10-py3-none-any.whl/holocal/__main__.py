import asyncio
import json
import logging
import sys
import urllib.request
from os import getenv

from dotenv import load_dotenv

import holocal

SLACK_WEBHOOK_URL = getenv("SLACK_WEBHOOK_URL")


class SlackWarningHandler(logging.Handler):
    def emit(self, record):
        if record.levelno == logging.WARNING:
            log_entry = self.format(record)
            payload = {
                "text": f":warning: {log_entry}"
            }

            if SLACK_WEBHOOK_URL:
                try:
                    req = urllib.request.Request(
                        url=SLACK_WEBHOOK_URL,
                        data=json.dumps(payload).encode('utf-8'),
                        headers={'Content-Type': 'application/json'},
                        method='POST'
                    )
                    with urllib.request.urlopen(req) as response:
                        if response.status != 200:
                            print(f"Slack webhook failed with status {response.status}")
                except Exception as e:
                    print(f"Failed to send Slack message: {e}")
            else:
                print("SLACK_WEBHOOK_URL environment variable is not set.")


load_dotenv()
logging.basicConfig(
    level=(getenv("HOLOCAL_LOGLEVEL") or "INFO").upper(),
    format="[{levelname}][{module}][{funcName}] {message}",
    style='{'
)

log = logging.getLogger()
slack_handler = SlackWarningHandler()
log.addHandler(slack_handler)

if __name__ == "__main__":
    # argparse いる？ 使わなそう…
    holocal_page = getenv(
        "HOLOCAL_PAGE") or "https://schedule.hololive.tv/simple"
    youtube_key = getenv("HOLOCAL_YOUTUBE_KEY")
    save_dir = getenv("HOLOCAL_DIR") or "public"

    if not holocal_page:
        log.critical("no holocal_page is given")
        sys.exit(1)

    if not youtube_key:
        log.critical("no youtube_key is given")
        sys.exit(1)

    assert youtube_key

    h = holocal.Holocal(holocal_page,
                        youtube_key, save_dir)
    sys.exit(asyncio.run(h.run()))
