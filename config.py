# config.py
import json

# API configurations can be stored in a separate JSON file
API_CONFIGS = {
    "bioscope": {
        "name": "Bioscope",
        "url": "https://api.staging.bioscopelive.com/v2/auth/login?country=BD&platform=web&language=en",
        "method": "POST",
        "payload": {"number": "+88{phone}"},
        "headers": {"Content-Type": "application/json"}
    },
    "bikroy": {
        "name": "Bikroy", 
        "url": "https://bikroy.com/data/phone_number_login/verifications/phone_login",
        "method": "POST",
        "payload": {"phone": "+88{phone}"},
        "headers": {"Content-Type": "application/json"}
    }
    # Add more APIs here...
}

def save_config(config, filename='api_config.json'):
    with open(filename, 'w') as f:
        json.dump(config, f, indent=2)

def load_config(filename='api_config.json'):
    with open(filename, 'r') as f:
        return json.load(f)
