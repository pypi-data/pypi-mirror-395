from __future__ import annotations

from enum import IntEnum

from common.message.base import Message
from common.message.color import Color
from common.message.point import Point2


class PointsAnnotationType(IntEnum):
    """
    Type of points annotation.
    """

    UNKNOWN = 0
    POINTS = 1
    LINE_LOOP = 2
    LINE_STRIP = 3
    LINE_LIST = 4


class CircleAnnotation(Message):
    """
    A circle annotation on a 2D image.

    Coordinates use the top-left corner of the top-left pixel as the origin.
    """

    timestamp_us: int
    position: Point2
    diameter: float
    thickness: float
    fill_color: Color
    outline_color: Color


class PointsAnnotation(Message):
    """
    An array of points on a 2D image.

    Coordinates use the top-left corner of the top-left pixel as the origin.
    """

    timestamp_us: int
    type: PointsAnnotationType
    points: list[Point2]
    outline_color: Color
    outline_colors: list[Color] | None = None
    fill_color: Color | None = None
    thickness: float


class TextAnnotation(Message):
    """
    A text label on a 2D image.

    Position uses the bottom-left origin of the text label.
    Coordinates use the top-left corner of the top-left pixel as the origin.
    """

    timestamp_us: int
    position: Point2
    text: str
    font_size: float
    text_color: Color
    background_color: Color


class ImageAnnotations(Message):
    """
    Array of annotations for a 2D image.

    Used in the Foxglove Image panel for visualization.
    """

    _type = "antioch/image_annotations"
    circles: list[CircleAnnotation]
    points: list[PointsAnnotation]
    texts: list[TextAnnotation]

    @classmethod
    def empty(cls) -> ImageAnnotations:
        """
        Create an empty ImageAnnotations instance.

        :return: ImageAnnotations with no annotations.
        """

        return cls(circles=[], points=[], texts=[])
