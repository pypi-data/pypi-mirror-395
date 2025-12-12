from typing import List, Optional
from pydantic import BaseModel, Field


class ChannelInfo(BaseModel):
    name: List[str]
    probe: Optional[List[str]] = Field(default_factory=list)
    units: Optional[List[str]] = Field(default_factory=list)
    analog_min: Optional[List[float]] = Field(default_factory=list)
    analog_max: Optional[List[float]] = Field(default_factory=list)
    digital_min: Optional[List[int]] = Field(default_factory=list)
    digital_max: Optional[List[int]] = Field(default_factory=list)
    prefiltering: Optional[List[str]] = Field(default_factory=list)
    number_of_points_per_channel: Optional[List[int]] = Field(default_factory=list)


class Header(BaseModel):
    type_before_conversion: str
    name_before_conversion: str
    creation_date_before_conversion: str
    creation_time_before_conversion: str
    sample_interval_microseconds: float
    number_of_channels: int
    number_of_sweeps: int = 1
    number_of_points_per_sweep: int = 0
    channel_info: ChannelInfo = Field(default_factory=ChannelInfo)
