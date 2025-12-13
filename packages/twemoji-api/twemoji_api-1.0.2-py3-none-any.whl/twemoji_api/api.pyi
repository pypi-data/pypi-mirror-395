from typing import List, FrozenSet, Optional, Union
from pathlib import Path

from emojis.db import Emoji
from twemoji_api.enum import PhotoType


def get_extension_folder(extension: Union[str, PhotoType]) -> Path:
    """
    Returns the Twemoji asset folder for the given extension.

    The filenames are identical in PNG and SVG directories;
    only the folder differs.

    Raises:
        ValidationError: If the extension value is invalid.
    """
    ...


def get_emoji_code_points(emoji: Union[str, Emoji]) -> List[str]:
    """
    Extract Unicode code points from the given emoji string or Emoji instance.

    Handles:
        • multi-codepoint emojis
        • variation selectors
        • skin-tone modifiers
        • ZWJ sequences

    Returns lowercase hex code points without the '0x' prefix.

    Raises:
        ValidationError: If the emoji input is invalid.
    """
    ...


def get_emojis_code_points_by_similarity(code_points: List[str]) -> FrozenSet[str]:
    """
    Returns all emoji filename stems whose code-point sets intersect
    with the provided list.

    Used to implement similarity lookups and fallback behavior.

    Does not perform validation on code_points; values are assumed to be
    valid lowercase hex strings.
    """
    ...


def get_emoji_code_points_by_similarity(code_points: List[str]) -> Optional[str]:
    """
    Returns the best matching emoji filename stem based on similarity.

    Similarity is determined by:
        • shared code points
        • prioritization of more specific sequences (longer stems)

    Returns:
        The matching filename stem, or None if no match is found.
    """
    ...


def get_emoji_path(
    emoji: Union[Emoji, str],
    extension: Union[str, PhotoType] = "png"
) -> Optional[Path]:
    """
    Resolves the local Twemoji asset path for the given emoji.

    Steps:
        • validate the emoji
        • derive its Unicode code points
        • attempt exact filename match
        • fallback to similarity-based match

    Returns:
        A Path object, or None if no file exists even after fallback.

    Raises:
        ValidationError: If the emoji or extension value is invalid.
    """
    ...


def get_emoji_url(
    emoji: Union[Emoji, str],
    extension: Union[str, PhotoType] = "png"
) -> Optional[str]:
    """
    Returns the GitHub raw URL to the corresponding Twemoji asset.

    Returns:
        A URL string, or None if the local file cannot be resolved.

    Raises:
        ValidationError: If the emoji or extension value is invalid.
    """
    ...


def get_all_emojis() -> List["Twemoji"]:
    """
    Returns a list of Twemoji objects representing every emoji present
    in the Twemoji PNG folder.

    All emojis in the Twemoji database are assumed valid; therefore no
    ValidationError is expected.
    """
    ...


class Twemoji:
    """
    High-level wrapper for emoji metadata and Twemoji asset resolution.

    Provides:
        • validated emoji object
        • Unicode code points
        • local asset path lookup
        • GitHub asset URL
    """

    _emoji: Emoji
    _extension: str

    def __init__(
        self,
        emoji: Union[Emoji, str],
        extension: Union[str, PhotoType] = "png"
    ) -> None:
        """
        Initializes a Twemoji object with validated values.

        Raises:
            ValidationError: If the emoji or extension are invalid.
        """
        ...

    @property
    def emoji(self) -> Emoji:
        """Returns the validated Emoji instance."""
        ...

    @emoji.setter
    def emoji(self, emoji: Union[Emoji, str]) -> None:
        """
        Sets and validates the emoji.

        Raises:
            ValidationError: If the value is not a valid emoji.
        """
        ...

    @property
    def extension(self) -> str:
        """Returns the resolved extension ('png' or 'svg')."""
        ...

    @extension.setter
    def extension(self, extension: Union[str, PhotoType]) -> None:
        """
        Sets and validates the extension.

        Raises:
            ValidationError: If the extension is invalid.
        """
        ...

    @property
    def code_points(self) -> List[str]:
        """
        Returns the emoji's Unicode code points.

        Raises:
            ValidationError: If the internal emoji is invalid (should not occur).
        """
        ...

    @property
    def path(self) -> Optional[Path]:
        """
        Local asset path, including fallback via similarity.

        Returns:
            A Path object or None.
        """
        ...

    @property
    def url(self) -> Optional[str]:
        """
        GitHub raw URL to the Twemoji asset.

        Returns:
            A URL string or None.
        """
        ...
