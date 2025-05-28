from flask import Flask, request, jsonify
import requests, datetime, os

app = Flask(__name__)
FIREBASE_URL = os.environ.get("https://slu-project-3bc4e-default-rtdb.firebaseio.com/sensor_data.json")  # e.g., https://your-app.firebaseio.com/data.json
FIREBASE_TOKEN = os.environ.get("https://your-project-id.firebaseio.com/sensor-data.json?auth=c0bGvEaNSVTyHNJbzQ9y5bvQqutkFCugMdXtvs6J")  # optional
@app.route('/')
def home():
    return 'Sensor logger is running.'
@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    try:
        data = request.json
        device_id = data['device_id']
        
        # Add timestamp
        data['timestamp'] = datetime.now().isoformat()
        
        # Store in Firebase
        ref = db.reference(f'sensors/{device_id}')
        ref.push().set(data)
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
