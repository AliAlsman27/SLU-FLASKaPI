from flask import Flask, request, jsonify
import os
import base64
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

app = Flask(__name__)

# Decode credentials from environment variable
cred_json = base64.b64decode(os.environ.get("FIREBASE_CREDENTIALS_B64")).decode("utf-8")
cred_dict = json.loads(cred_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-project.firebaseio.com'
})

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
