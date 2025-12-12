from collections.abc import Sequence

from ytrssil.api import get_new_video_count, get_new_videos
from ytrssil.datatypes import Video

__all__: Sequence[str] = (
    'Video',
    'get_new_video_count',
    'get_new_videos',
)
