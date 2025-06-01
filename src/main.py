from fastapi import FastAPI, HTTPException, Request
from firebase_admin import db
from datetime import datetime
from models import SensorData
from config import init_firebase

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
        print("Received data:", sensor_data)
        timestamp = datetime.now().isoformat()
        
        # Add timestamp to each reading (handle both dict and Pydantic model)
        updated_data = []
        for reading in sensor_data.data:
            if hasattr(reading, "copy"):
                # Pydantic model
                updated = reading.copy(update={"timestamp": timestamp})
                updated_data.append(updated)
            elif isinstance(reading, dict):
                # dict
                reading['timestamp'] = timestamp
                updated_data.append(reading)
            else:
                # fallback
                updated_data.append(reading)

        # Save to Firebase
        ref = db.reference(f'sensors/{sensor_data.device_id}')
        ref.set({
            'device_id': sensor_data.device_id,
            'data': [r.dict() if hasattr(r, "dict") else r for r in updated_data],
            'timestamp': timestamp
        })

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sensor-data/debug")
async def debug_sensor_data(request: Request):
    try:
        data = await request.json()
        print("Raw received JSON:", data)
        return {"received": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
