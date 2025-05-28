from flask import Flask, request, jsonify
import requests, datetime, os, json
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)
# Load credentials from environment variable
cred_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")

if not cred_json:
    raise RuntimeError("FIREBASE_CREDENTIALS_JSON is not set.")

cred_dict = json.loads(cred_json)

# Initialize the Firebase app
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://slu-project-3bc4e-default-rtdb.firebaseio.com/'  # ← replace with your real Firebase URL
    })
@app.route('/')
def home():
    return 'Sensor logger is running.'
@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    try:
        data = request.json
        device_id = data['device_id']
        
        # Add timestamp
        data['timestamp'] = datetime.datetime.now().isoformat()

        
        # Store in Firebase
        ref = db.reference(f'sensors/{device_id}')
        ref.push().set(data)
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
