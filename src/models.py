from typing import List, Optional, Union
from pydantic import BaseModel
from datetime import datetime

class SensorReading(BaseModel):
    sensor: str
    value: Union[int, float, List[float]]  # Modified to accept list of floats for GPS
    unit: str
    timestamp: Optional[datetime] = None  # Optional, will be set on server side

class SensorData(BaseModel):
    device_id: str
    status: str  # New field for device status
    data: List[SensorReading]
