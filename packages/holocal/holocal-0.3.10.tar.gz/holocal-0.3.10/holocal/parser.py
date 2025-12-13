import csv
import datetime
import html.parser
import logging
import re
from enum import StrEnum

from holocal.errors import HolocalException
from holocal.event import Event, Talent
from holocal.site import Site

SPACES_WITH_NEWLINES = r"[ \r]*\n[ \n\r]*"
DATE = r"(?P<month>\d\d)/(?P<day>\d\d)"
TIME = r"(?P<hour>\d\d):(?P<minute>\d\d)"

GROUPS = ["holo EN",
          "FLOW GLOW",
          "ReGLOSS",
          "ホロライブ",
          "ホロスターズ",
          "HOLOSTARS EN",
          "holo ID",
          "ホロカ公式"]

log = logging.getLogger(__name__)

marks = {}
with open("marks.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        marks[row["talent"]] = row["mark"]


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self._date = None
        self.current_hyperlink = None
        self._state = State.OUTSIDE
        self._tags = []
        self.events = []
        self._reset_current_link()

    def handle_starttag(self, tag: str, attrs: list) -> None:
        match self._state:
            case State.OUTSIDE if dict(attrs).get("id") == "all":
                self._state = State.INSIDE

            case State.INSIDE if tag == "a":
                self._tags.append(tag)
                self.current_hyperlink = dict(attrs)["href"]
                self._state = State.ANCHOR

            case State.INSIDE if tag == "div" \
                                 and dict(attrs).get("class") == "holodule navbar-text":
                self._tags.append(tag)
                self._state = State.DATE

            case State.INSIDE:
                self._tags.append(tag)

            case State.ANCHOR if tag != "img":
                self._tags.append(tag)

            case State.OUTSIDE | State.ANCHOR | State.REST:
                pass

    def handle_data(self, data):
        match self._state:
            case State.ANCHOR:
                self.current_text += data

            case State.DATE:
                match data.split():
                    case [date, _]:
                        match = re.match(DATE, date)
                        if not match:
                            raise HolocalException(repr(date))

                        self._date = Date(int(match["month"]),
                                          int(match["day"]))

    def handle_endtag(self, tag):
        match self._state:
            case State.INSIDE if not self._tags:
                self._state = State.REST

            case State.INSIDE if tag == self._tags.pop():
                pass

            case State.ANCHOR if self._tags.pop() == tag and tag == "a":
                self._parse_anchor_text()
                self._reset_current_link()
                self._state = State.INSIDE

            case State.DATE if self._tags.pop() == tag:
                self._state = State.INSIDE

            case State.ANCHOR | State.OUTSIDE | State.REST:
                pass

    def _reset_current_link(self):
        self.current_hyperlink = None
        self.current_text = ""

    def _parse_anchor_text(self):
        match re.split(SPACES_WITH_NEWLINES, self.current_text):
            case ['', time, talent, '']:
                mark = marks.get(talent)

                if mark:
                    log.debug(f"registered mark: {mark}")
                    self._validate_time(time)
                    self._append_link(url=self.current_hyperlink,
                                      talent=Talent(talent, mark))
                    return

                if talent not in GROUPS:
                    log.warning(f"no mark found for {repr(talent)}")

                self._validate_time(time)
                self._append_link(url=self.current_hyperlink,
                                  talent=Talent(talent))

            case ['', time, talent, mark, '']:
                self._validate_time(time)
                self._append_link(url=self.current_hyperlink,
                                  talent=Talent(talent, mark))

            case _:
                raise HolocalException(f"text: {repr(self.current_text)}")

    def _validate_time(self, time):
        match = re.match(TIME, time)
        if not match:
            raise HolocalException(repr(time))

        year = int(match["hour"])
        minute = int(match["minute"])
        time = Time(year, minute)
        self._time = time

    def _append_link(self, url, talent):
        year = datetime.datetime.now().year
        timezone = datetime.timezone(datetime.timedelta(hours=9))
        time = datetime.datetime(year,
                                 self._date.month,
                                 self._date.day,
                                 self._time.hour,
                                 self._time.minute,
                                 tzinfo=timezone)
        time = time.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
        self.events.append(Event(site=Site.parse_url(url),
                                 talent=talent,
                                 date_time=time))


class Date:
    def __init__(self, month, day):
        self.month = month
        self.day = day


class Time:
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute


class State(StrEnum):
    OUTSIDE = "outside of anchors"
    INSIDE = "inside of anchors"
    ANCHOR = "reading anchor text"
    REST = "rest, after anchors"
    DATE = "date"
