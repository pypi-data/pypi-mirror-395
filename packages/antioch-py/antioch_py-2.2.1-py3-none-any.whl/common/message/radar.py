from pydantic import Field

from common.message.base import Message
from common.message.point_cloud import PointCloud
from common.message.vector import Vector3


class RadarDetection(Message):
    """
    Single radar detection point with position and properties.
    """

    _type = "antioch/radar_detection"
    position: Vector3 = Field(description="3D position of detection in sensor frame")
    range: float = Field(description="Range to target in meters")
    azimuth: float = Field(description="Azimuth angle in radians")
    elevation: float = Field(description="Elevation angle in radians")
    velocity: float = Field(default=0.0, description="Radial velocity in m/s (positive = moving away)")
    rcs: float = Field(default=0.0, description="Radar cross section in dBsm")


class RadarScan(Message):
    """
    Radar scan data containing all detections from a single scan.
    """

    _type = "antioch/radar_scan"
    detections: list[RadarDetection] = Field(default_factory=list, description="List of radar detections")

    def to_point_cloud(self, frame_id: str = "radar") -> PointCloud:
        """
        Convert radar scan to a point cloud.

        :param frame_id: Frame of reference for the point cloud.
        :return: PointCloud with detection positions.
        """

        if not self.detections:
            return PointCloud(frame_id=frame_id, x=[], y=[], z=[])

        return PointCloud(
            frame_id=frame_id,
            x=[d.position.x for d in self.detections],
            y=[d.position.y for d in self.detections],
            z=[d.position.z for d in self.detections],
        )

    @staticmethod
    def combine(scans: list["RadarScan"]) -> "RadarScan":
        """
        Combine multiple radar scans into a single scan.

        :param scans: List of radar scans to combine.
        :return: Combined radar scan with all detections.
        """

        detections = sum((scan.detections for scan in scans), [])
        return RadarScan(detections=detections)
