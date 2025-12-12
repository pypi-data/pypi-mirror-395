from __future__ import annotations

from pydantic import field_validator

from common.message.base import Message


class Color(Message):
    """
    An RGBA color with values in the range [0.0, 1.0].

    Used in image annotations and visualization.
    """

    _type = "antioch/color"
    r: float
    g: float
    b: float
    a: float

    @field_validator("r", "g", "b", "a")
    @classmethod
    def validate_range(cls, v: float) -> float:
        """
        Validate that color values are in the range [0.0, 1.0].

        :param v: The color value to validate.
        :return: The validated color value.
        :raises ValueError: If the value is not in [0.0, 1.0].
        """

        if not 0.0 <= v <= 1.0:
            raise ValueError(f"Color values must be in range [0.0, 1.0], got {v}")
        return v

    def __repr__(self) -> str:
        """
        Return a readable string representation.

        :return: String representation.
        """

        return f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})"

    def __str__(self) -> str:
        """
        Return a readable string representation.

        :return: String representation.
        """

        return f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})"

    @classmethod
    def rgba(cls, r: float, g: float, b: float, a: float = 1.0) -> Color:
        """
        Create a color from RGBA values.

        :param r: Red component [0.0, 1.0].
        :param g: Green component [0.0, 1.0].
        :param b: Blue component [0.0, 1.0].
        :param a: Alpha component [0.0, 1.0]. Defaults to 1.0 (opaque).
        :return: A Color instance.
        """

        return cls(r=r, g=g, b=b, a=a)

    @classmethod
    def rgb(cls, r: float, g: float, b: float) -> Color:
        """
        Create an opaque color from RGB values.

        :param r: Red component [0.0, 1.0].
        :param g: Green component [0.0, 1.0].
        :param b: Blue component [0.0, 1.0].
        :return: A Color instance with alpha = 1.0.
        """

        return cls(r=r, g=g, b=b, a=1.0)

    @classmethod
    def red(cls) -> Color:
        """
        Create a red color.

        :return: Red color (1.0, 0.0, 0.0, 1.0).
        """

        return cls(r=1.0, g=0.0, b=0.0, a=1.0)

    @classmethod
    def green(cls) -> Color:
        """
        Create a green color.

        :return: Green color (0.0, 1.0, 0.0, 1.0).
        """

        return cls(r=0.0, g=1.0, b=0.0, a=1.0)

    @classmethod
    def blue(cls) -> Color:
        """
        Create a blue color.

        :return: Blue color (0.0, 0.0, 1.0, 1.0).
        """

        return cls(r=0.0, g=0.0, b=1.0, a=1.0)

    @classmethod
    def white(cls) -> Color:
        """
        Create a white color.

        :return: White color (1.0, 1.0, 1.0, 1.0).
        """

        return cls(r=1.0, g=1.0, b=1.0, a=1.0)

    @classmethod
    def black(cls) -> Color:
        """
        Create a black color.

        :return: Black color (0.0, 0.0, 0.0, 1.0).
        """

        return cls(r=0.0, g=0.0, b=0.0, a=1.0)

    @classmethod
    def transparent(cls) -> Color:
        """
        Create a transparent color.

        :return: Transparent color (0.0, 0.0, 0.0, 0.0).
        """

        return cls(r=0.0, g=0.0, b=0.0, a=0.0)
