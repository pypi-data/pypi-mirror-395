from pydantic import Field

from common.message.base import Message
from common.message.quaternion import Quaternion
from common.message.vector import Vector3


class FrameTransform(Message):
    """
    A transform between two reference frames in 3D space.

    :param parent_frame_id: Name of the parent frame.
    :param child_frame_id: Name of the child frame.
    :param translation: Translation component of the transform.
    :param rotation: Rotation component of the transform.
    """

    _type = "antioch/frame_transform"
    parent_frame_id: str = Field(description="Name of the parent frame")
    child_frame_id: str = Field(description="Name of the child frame")
    translation: Vector3 = Field(description="Translation component of the transform")
    rotation: Quaternion = Field(description="Rotation component of the transform")

    @classmethod
    def identity(cls, parent_frame_id: str, child_frame_id: str) -> "FrameTransform":
        """
        Create an identity transform between two frames.

        :param parent_frame_id: Name of the parent frame.
        :param child_frame_id: Name of the child frame.
        :return: Identity frame transform.
        """

        return cls(
            parent_frame_id=parent_frame_id,
            child_frame_id=child_frame_id,
            translation=Vector3.zeros(),
            rotation=Quaternion.identity(),
        )


class FrameTransforms(Message):
    """
    An array of FrameTransform messages.

    :param transforms: Array of transforms.
    """

    _type = "antioch/frame_transforms"
    transforms: list[FrameTransform] = Field(default_factory=list, description="Array of transforms")
