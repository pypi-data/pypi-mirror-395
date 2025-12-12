from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Video:
    video_id: str
    title: str
    channel_name: str
    published_timestamp: datetime
    short: bool
    watch_timestamp: Optional[datetime] = None

    def __str__(self) -> str:
        return f"{self.channel_name} - {self.title} - {self.video_id}"


@dataclass
class Channel:
    channel_id: str
    name: str

    def __str__(self) -> str:
        return f"{self.name} - {self.channel_id}"
