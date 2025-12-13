import struct

from pydantic import Field, model_validator

from common.message.base import Message


class PointCloud(Message):
    """
    A collection of 3D points.

    :param frame_id: Frame of reference.
    :param x: X coordinates of points.
    :param y: Y coordinates of points.
    :param z: Z coordinates of points.
    """

    _type = "antioch/point_cloud"
    frame_id: str = Field(default="", description="Frame of reference")
    x: list[float] = Field(description="X coordinates of points")
    y: list[float] = Field(description="Y coordinates of points")
    z: list[float] = Field(description="Z coordinates of points")

    @model_validator(mode="after")
    def validate_array_lengths(self) -> "PointCloud":
        """
        Validate that all coordinate arrays have the same length.
        """

        lengths = [len(self.x), len(self.y), len(self.z)]

        if len(set(lengths)) > 1:
            raise ValueError(f"All coordinate arrays must have the same length: x={len(self.x)}, y={len(self.y)}, z={len(self.z)}")

        return self

    def to_bytes(self) -> bytes:
        """
        Pack point cloud data into bytes for Foxglove.

        :return: Packed data with x, y, z for each point.
        """

        data = bytearray()
        for i in range(len(self.x)):
            data.extend(struct.pack("<fff", self.x[i], self.y[i], self.z[i]))

        return bytes(data)

    @staticmethod
    def combine(point_clouds: list["PointCloud"], frame_id: str = "") -> "PointCloud":
        """
        Combine multiple point clouds into a single point cloud.

        :param point_clouds: List of point clouds to combine.
        :param frame_id: Frame of reference for the combined point cloud.
        :return: Combined point cloud with all points.
        """

        all_x = sum((pc.x for pc in point_clouds), [])
        all_y = sum((pc.y for pc in point_clouds), [])
        all_z = sum((pc.z for pc in point_clouds), [])
        return PointCloud(frame_id=frame_id, x=all_x, y=all_y, z=all_z)
