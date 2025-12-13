# Twemoji API

A lightweight utility for resolving emojis into file names, local asset paths, and URLs.
Supports both **PNG** and **SVG** assets using the Twemoji standard.

## Features

* Convert emojis to Unicode-based file names
* Retrieve local file paths for emoji assets
* Get direct URLs to Twemoji files
* Supports **PNG** and **SVG**

## Installation

```bash
pip install twemoji-api
```

## Usage

```python
from twemoji_api import get_emoji_path, get_emoji_url, Twemoji

print(get_emoji_path("🔥"))
print(get_emoji_url("🔥"))

emoji = Twemoji("🔥")
print(emoji.file_name)
print(emoji.path)
print(emoji.url)
```

## Functions

### `get_emoji_path(emoji, extension="png")`

Returns the local path for the emoji file.

### `get_emoji_url(emoji, extension="png")`

Returns the URL to the emoji file.

### `get_emoji_file_name(emoji)`

Converts the emoji into its Unicode filename format.

### `Twemoji`

Object-oriented interface providing:

* `file_name`
* `path`
* `url`

## License

MIT


## Twemoji Attribution

This project includes graphics from Twemoji.
Copyright 2019 Twitter, Inc and other contributors.
Licensed under CC-BY 4.0:
https://creativecommons.org/licenses/by/4.0/
No changes were made.