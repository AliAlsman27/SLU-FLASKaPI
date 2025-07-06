import os
import json
from firebase_admin import credentials, initialize_app
from pathlib import Path

def init_firebase():
    try:
        # First try environment variable
        cred_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
        
        # If not in env var, try local file for development
        if not cred_json:
            cred_path = Path(__file__).parent.parent / 'firebase-credentials.json'
            if cred_path.exists():
                with open(cred_path, 'r') as f:
                    cred_json = f.read()
            else:
                raise RuntimeError(
                    "Firebase credentials not found. Either:\n"
                    "1. Set FIREBASE_CREDENTIALS_JSON environment variable, or\n"
                    "2. Create firebase-credentials.json in project root"
                )
        
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        initialize_app(cred, {
            'databaseURL': 'https://slu-project-3bc4e-default-rtdb.firebaseio.com/'
        })
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Firebase: {str(e)}")
