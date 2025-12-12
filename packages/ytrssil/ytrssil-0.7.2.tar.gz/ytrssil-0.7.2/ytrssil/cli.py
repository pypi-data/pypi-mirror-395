from collections.abc import Iterator
from os import execv, fork
from subprocess import PIPE, Popen
from sys import argv, stderr
from typing import Any

from inject import autoparams

from ytrssil.bindings import setup_dependencies
from ytrssil.config import Configuration
from ytrssil.datatypes import Video
from ytrssil.protocols import Client


def user_query(videos: list[Video], reverse: bool = False) -> list[str]:
    p = Popen(
        ["fzf", "-m"],
        stdout=PIPE,
        stdin=PIPE,
    )
    video_list: Iterator[Video]
    if reverse:
        video_list = reversed(videos)
    else:
        video_list = iter(videos)

    input_bytes = "\n".join(map(str, video_list)).encode("UTF-8")
    stdout, _ = p.communicate(input=input_bytes)
    videos_str: list[str] = stdout.decode("UTF-8").strip().split("\n")
    ret: list[str] = []
    for video_str in videos_str:
        if video_str == "":
            continue

        *_, video_id = video_str.split(" - ")

        try:
            ret.append(video_id)
        except KeyError:
            pass

    return ret


@autoparams()
def fetch(client: Client) -> int:
    client.fetch()
    return 0


@autoparams()
def register(client: Client) -> int:
    client.register()
    return 0


@autoparams("client")
def subscribe_to_channel(client: Client, channel_id: str) -> int:
    client.subscribe_to_channel(channel_id)
    return 0


@autoparams()
def watch_videos(config: Configuration, client: Client) -> int:
    videos = client.get_new_videos()
    if not videos:
        print("No new videos", file=stderr)
        return 1

    selected_videos = user_query(videos)
    if not selected_videos:
        print("No video selected", file=stderr)
        return 2

    video_urls = [
        f"https://www.youtube.com/watch?v={video_id}" for video_id in selected_videos
    ]
    cmd = ["/usr/bin/mpv", *config.mpv_options, *video_urls]
    if fork() == 0:
        execv(cmd[0], cmd)

    for video_id in selected_videos:
        client.mark_video_as_watched(video_id)

    return 0


@autoparams()
def print_url(client: Client) -> int:
    videos = client.get_new_videos()
    if not videos:
        print("No new videos", file=stderr)
        return 1

    selected_videos = user_query(videos)
    if not selected_videos:
        print("No video selected", file=stderr)
        return 2

    for video_id in selected_videos:
        client.mark_video_as_watched(video_id)
        print(f"https://www.youtube.com/watch?v={video_id}")

    return 0


@autoparams()
def mark_as_watched(client: Client) -> int:
    videos = client.get_new_videos()
    if not videos:
        print("No new videos", file=stderr)
        return 1

    selected_videos = user_query(videos)
    if not selected_videos:
        print("No video selected", file=stderr)
        return 2

    for video_id in selected_videos:
        client.mark_video_as_watched(video_id)

    return 0


@autoparams()
def watch_history(config: Configuration, client: Client) -> int:
    videos = client.get_watched_videos()
    if not videos:
        print("No new videos", file=stderr)
        return 1

    selected_videos = user_query(videos)
    if not selected_videos:
        print("No video selected", file=stderr)
        return 2

    video_urls = [
        f"https://www.youtube.com/watch?v={video_id}" for video_id in selected_videos
    ]
    cmd = ["/usr/bin/mpv", *config.mpv_options, *video_urls]
    if fork() == 0:
        execv(cmd[0], cmd)

    return 0


@autoparams()
def mark_as_unwatched(client: Client) -> int:
    videos = client.get_watched_videos()
    if not videos:
        print("No new videos", file=stderr)
        return 1

    selected_videos = user_query(videos)
    if not selected_videos:
        print("No video selected", file=stderr)
        return 2

    for video_id in selected_videos:
        client.mark_video_as_unwatched(video_id)

    return 0


def main(args: list[str] = argv) -> Any:
    setup_dependencies()
    command: str
    try:
        command = args[1]
    except IndexError:
        command = "watch"

    if command == "fetch":
        return fetch()
    elif command == "register":
        return register()
    elif command == "subscribe":
        if len(args) < 3:
            print(
                "Missing channel ID argument for subscribe command",
                file=stderr,
            )
            return 1

        return subscribe_to_channel(channel_id=args[2])
    elif command == "watch":
        return watch_videos()
    elif command == "print":
        return print_url()
    elif command == "history":
        return watch_history()
    elif command == "mark":
        return mark_as_watched()
    elif command == "unmark":
        return mark_as_unwatched()
    else:
        print(f'Unknown command "{command}"', file=stderr)
        print(
            "Available commands: fetch, watch, print, history, mark, unmark",
            file=stderr,
        )
        return 1

    return 0
