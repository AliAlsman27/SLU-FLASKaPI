from fastapi import FastAPI, HTTPException
from firebase_admin import db
from datetime import datetime
from .models import SensorData
from .config import init_firebase

app = FastAPI(title="Sensor Logger API")

@app.on_event("startup")
async def startup_event():
    init_firebase()

@app.get("/")
async def home():
    return {"message": "Sensor logger is running"}

@app.post("/api/sensor-data")
async def receive_sensor_data(sensor_data: SensorData):
    try:
        timestamp = datetime.now().isoformat()
        
        # Add timestamp to each reading
        for reading in sensor_data.data:
            reading.timestamp = timestamp

        # Save to Firebase
        ref = db.reference(f'sensors/{sensor_data.device_id}')
        ref.set({
            'device_id': sensor_data.device_id,
            'data': [reading.dict() for reading in sensor_data.data],
            'timestamp': timestamp
        })

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
