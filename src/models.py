from typing import List
from pydantic import BaseModel
from datetime import datetime

class SensorReading(BaseModel):
    value: float
    type: str
    unit: str = "unknown"
    timestamp: datetime | None = None

class SensorData(BaseModel):
    device_id: str
    data: List[SensorReading]
