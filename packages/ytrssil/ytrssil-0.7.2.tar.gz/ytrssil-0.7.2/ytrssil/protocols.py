from typing import Protocol

from ytrssil.datatypes import Video


class Client(Protocol):
    def fetch(self) -> None:  # pragma: no cover
        ...

    def register(self) -> None:  # pragma: no cover
        ...

    def subscribe_to_channel(
        self,
        channel_id: str,
    ) -> None:  # pragma: no cover
        ...

    def get_new_videos(self) -> list[Video]:  # pragma: no cover
        ...

    def get_watched_videos(self) -> list[Video]:  # pragma: no cover
        ...

    def mark_video_as_watched(self, video_id: str) -> None:  # pragma: no cover
        ...

    def mark_video_as_unwatched(
        self,
        video_id: str,
    ) -> None:  # pragma: no cover
        ...
