# YouTube RSS manager

This is a simple CLI to manage YouTube subscriptions through RSS feeds
and watch new videos using `mpv`.

## Configuration

It looks for a configuration in `$XDG_CONFIG_HOME/ytrssil/config.json`
(~/.config/ by default).

Example:

```json
{
    "token": "token",
    "api_url": "https://example.com",
    "max_resolution": "1080"
}
```
