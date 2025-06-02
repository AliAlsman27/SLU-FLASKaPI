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
        
        # Add timestamp to each reading, matching ESP32 schema
        updated_data = []
        for reading in sensor_data.data:
            # Convert to dict if it's a Pydantic model
            if hasattr(reading, "dict"):
                reading = reading.dict()
            # Only keep expected keys and add timestamp
            filtered = {
                "sensor": reading.get("sensor"),
                "value": reading.get("value"),
                "unit": reading.get("unit"),
                "timestamp": timestamp
            }
            updated_data.append(filtered)

        # Save to Firebase
        ref = db.reference(f'stations/{sensor_data.device_id}')
        ref.set({
            'device_id': sensor_data.device_id,
            'data': updated_data,
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
