from typing import cast

from inject import autoparams

from ytrssil.bindings import setup_dependencies
from ytrssil.datatypes import Video
from ytrssil.protocols import Client


def get_new_videos() -> list[Video]:
    setup_dependencies()

    @autoparams()
    def _get_new_videos(client: Client) -> list[Video]:
        return client.get_new_videos()

    return cast(list[Video], _get_new_videos())


def get_new_video_count() -> int:
    return len(get_new_videos())
