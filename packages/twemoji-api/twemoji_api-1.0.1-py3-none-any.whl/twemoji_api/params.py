import typing

import emojis
from emojis.db import Emoji, get_emoji_by_code
from pydantic import BaseModel, field_validator

from twemoji_api.enum import PhotoType


class EmojiParams(BaseModel):
    emoji: typing.Union[Emoji, str]

    @field_validator("emoji", mode="before")
    def load_emoji(cls, v):
        if isinstance(v, Emoji):
            return v
        elif isinstance(v, str):
            emoji = emojis.get(v)
            if len(emoji) == 1:
                emoji = next(iter(emoji))
                return get_emoji_by_code(emoji)
            else:
                raise ValueError("Only one emoji allowed.")
        else:
            raise TypeError("Invalid type for emoji.")


class ExtensionParams(BaseModel):
    extension: PhotoType