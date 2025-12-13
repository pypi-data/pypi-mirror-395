from pathlib import Path

from twemoji_api.params import ExtensionParams, EmojiParams


def get_emoji_path(emoji, extension = "png"):
    ExtensionParams(extension=extension)
    file_name = get_emoji_file_name(emoji)
    if extension == "svg":
        folder = "svg"
    else:
        folder = "72x72"
    path = Path(__file__).parent.absolute() / f"assets/{folder}/{file_name}.{extension}"
    return path


def get_emoji_url(emoji, extension = "png"):
    path = get_emoji_path(emoji, extension)
    folder = path.parent.name
    return f"https://github.com/jdecked/twemoji/blob/main/assets/{folder}/{path.name}"


def get_emoji_file_name(emoji):
    emoji_params = EmojiParams(emoji=emoji)
    emoji = emoji_params.emoji
    delimiter = "-"
    # Convert the string into a list of UTF-16 code units
    code_units = [ord(char) for char in emoji.emoji]

    # Process the code units in pairs (high surrogate + low surrogate)
    code_points = []
    i = 0
    while i < len(code_units):
        high_surrogate = code_units[i]
        low_surrogate = code_units[i + 1] if i + 1 < len(code_units) else None

        # Check if the current pair is a valid surrogate pair
        if 0xD800 <= high_surrogate <= 0xDBFF and 0xDC00 <= low_surrogate <= 0xDFFF:
            # Calculate the code point
            code_point = (
                    ((high_surrogate - 0xD800) << 10)
                    + (low_surrogate - 0xDC00)
                    + 0x10000
            )
            code_points.append(hex(code_point)[2:])  # Remove the '0x' prefix
            i += 2  # Move to the next pair
        else:
            # If not a surrogate pair, treat it as a regular code point
            code_points.append(hex(high_surrogate)[2:])
            i += 1

    # Join the code points with the specified delimiter
    return delimiter.join(code_points)


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
    def file_name(self):
        return get_emoji_file_name(self.emoji)

    @property
    def url(self):
        return get_emoji_url(self.emoji, self.extension)
