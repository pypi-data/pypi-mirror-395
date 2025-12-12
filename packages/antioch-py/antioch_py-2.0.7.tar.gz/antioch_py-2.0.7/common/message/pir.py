from pydantic import Field

from common.message.base import Message


class PirStatus(Message):
    """
    PIR sensor status containing detection state and signal information.
    """

    _type = "antioch/pir_status"
    is_detected: bool = Field(description="Whether motion is currently detected (aggregated across all sensors)")
    signal_strength: float = Field(description="Max absolute signal strength across all sensors")

    # Multi-sensor status
    sensor_states: list[bool] = Field(default_factory=list, description="Detection state per sensor (Center, Left, Right)")
    sensor_signals: list[float] = Field(default_factory=list, description="Signal strength per sensor")
    sensor_thresholds: list[float] = Field(default_factory=list, description="Detection threshold per sensor")
