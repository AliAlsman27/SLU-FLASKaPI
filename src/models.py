from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class SensorReading(BaseModel):
    sensor: str
    value: float
    unit: str
    raw_distance: float
    raw_unit: str
    timestamp: Optional[str] = None  # Make timestamp optional

class SensorData(BaseModel):
    device_id: str
    data: List[SensorReading]
