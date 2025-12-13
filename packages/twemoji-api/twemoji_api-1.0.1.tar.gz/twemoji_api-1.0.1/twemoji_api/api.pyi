import typing
from pathlib import Path

from emojis.db import Emoji

from twemoji_api.enum import PhotoType
from twemoji_api.params import EmojiParams, ExtensionParams


def get_emoji_path(emoji: typing.Union[Emoji, str], extension: typing.Union[PhotoType, str] = ...) -> Path:
    """
    Get the path of the given emoji.
    :param emoji: Emoji object
    :param extension: file extension
    :return: Emoji path
    """
    ...

def get_emoji_url(emoji: typing.Union[Emoji, str], extension: typing.Union[PhotoType, str] = ...) -> str:
    """
    Get the github url of the given emoji.
    :param emoji: Emoji object
    :param extension: file extension
    :return: Emoji github url
    """


def get_emoji_file_name(emoji: typing.Union[Emoji, str]) -> str:
    """
    Get the file name of the given emoji.
    :param emoji: Emoji object
    :return: Emoji name
    """
    ...


class Twemoji:
    def __init__(self, emoji: typing.Union[Emoji, str], extension: typing.Union[PhotoType, str] = ...):
        self.emoji = emoji
        self.extension = extension

    @property
    def emoji(self) -> Emoji:
        return self._emoji

    @emoji.setter
    def emoji(self, emoji: typing.Union[Emoji, str]) -> None:
        emoji_params = EmojiParams(emoji=emoji)
        self._emoji = emoji_params.emoji

    @property
    def extension(self) -> str:
        return self._extension

    @extension.setter
    def extension(self, extension: typing.Union[PhotoType, str]) -> None:
        ExtensionParams(extension=extension)
        self._extension = extension

    @property
    def path(self) -> Path:
        return get_emoji_path(self.emoji, self.extension)

    @property
    def file_name(self) -> str:
        return get_emoji_file_name(self.emoji)

    @property
    def url(self) -> str:
        return get_emoji_url(self.emoji, self.extension)
