from typing import List, Optional, Union
from pydantic import BaseModel
from datetime import datetime

class SensorReading(BaseModel):
    sensor: str
    value: Union[int, float]
    unit: str
    timestamp: Optional[datetime] = None  # Optional, will be set on server side

class SensorData(BaseModel):
    device_id: str
    data: List[SensorReading]
