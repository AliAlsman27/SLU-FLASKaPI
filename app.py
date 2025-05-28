from flask import Flask, request, jsonify
import os, json, datetime
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Load Firebase credentials from environment variable
cred_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
if not cred_json:
    raise RuntimeError("FIREBASE_CREDENTIALS_JSON is not set.")

cred_dict = json.loads(cred_json)

# Initialize Firebase app
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://slu-project-3bc4e-default-rtdb.firebaseio.com/'
    })

@app.route('/')
def home():
    return 'Sensor logger is running.'

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    try:
        print("🔥 Headers:", dict(request.headers))
        print("🔥 Body:", request.get_data(as_text=True))

        data = request.get_json(force=True)

        if 'device_id' not in data or 'data' not in data:
            raise ValueError("Missing required fields: 'device_id' or 'data'.")

        device_id = data['device_id']
        readings = data['data']
        timestamp = datetime.datetime.now().isoformat()

        # Attach timestamp to each reading
        for entry in readings:
            entry['timestamp'] = timestamp
            if 'unit' not in entry:
                entry['unit'] = 'unknown'  # Optional default

        # Save to Firebase under sensors/<device_id>
        ref = db.reference(f'sensors/{device_id}')
        ref.push({
            'device_id': device_id,
            'data': readings,
            'timestamp': timestamp
        })

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
