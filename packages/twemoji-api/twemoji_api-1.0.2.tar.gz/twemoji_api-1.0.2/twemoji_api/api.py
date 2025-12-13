from pathlib import Path

from twemoji_api.params import ExtensionParams, EmojiParams
from emojis.db.db import EMOJI_DB


def get_extension_folder(extension):
    ExtensionParams(extension=extension)
    if extension == "svg":
        folder = "svg"
    else:
        folder = "72x72"
    return Path(__file__).parent.absolute() / f"assets/{folder}"


def _build_index():
    folder = get_extension_folder("png")
    return dict(map(lambda f: (frozenset(f.stem.split("-")), f.stem), folder.iterdir()))


_EMOJI_INDEX = _build_index()


def get_emoji_path(emoji, extension = "png"):
    folder = get_extension_folder(extension)
    code_points = get_emoji_code_points(emoji)
    file_name = "-".join(code_points)
    path = folder / f"{file_name}.{extension}"
    if path.exists():
        return path
    else:
        other_code_points = get_emoji_code_points_by_similarity(code_points)
        if other_code_points:
            path = folder / f"{other_code_points}.{extension}"
            if path.exists():
                return path
        return None


def get_emojis_code_points_by_similarity(code_points):
    target = frozenset(code_points)
    return frozenset(map(lambda v: v[1], filter(lambda v: v[0].issubset(target), _EMOJI_INDEX.items())))


def get_emoji_code_points_by_similarity(code_points):
    matches = get_emojis_code_points_by_similarity(code_points)
    return next(iter(matches), None)


def get_emoji_url(emoji, extension = "png"):
    path = get_emoji_path(emoji, extension)
    if path is None:
        return None
    folder = path.parent.name
    return f"https://raw.githubusercontent.com/twitter/twemoji/master/assets/{folder}/{path.name}"


def get_emoji_code_points(emoji):
    params = EmojiParams(emoji=emoji)
    return [hex(ord(ch)).replace("0x", "") for ch in params.emoji.emoji]


def get_all_emojis(extension = "png"):
    return list(map(lambda e: Twemoji(e, extension), EMOJI_DB))


class Twemoji:
    def __init__(self, emoji, extension = 'png'):
        self.emoji = emoji
        self.extension = extension

    @property
    def emoji(self):
        return self._emoji

    @emoji.setter
    def emoji(self, emoji):
        emoji_params = EmojiParams(emoji=emoji)
        self._emoji = emoji_params.emoji

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, extension):
        ExtensionParams(extension=extension)
        self._extension = extension

    @property
    def path(self):
        return get_emoji_path(self.emoji, self.extension)

    @property
    def code_points(self):
        return get_emoji_code_points(self.emoji)

    @property
    def url(self):
        return get_emoji_url(self.emoji, self.extension)
