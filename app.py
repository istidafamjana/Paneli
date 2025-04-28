from flask import Flask, request, jsonify, abort
import json
import os

app = Flask(__name__)

API_KEY_NAME = "X-API-KEY"
KEYS_FILE = "keys.json"

# تحميل المفاتيح من ملف JSON
def load_keys():
    if not os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, 'w') as f:
            json.dump({}, f)
    with open(KEYS_FILE, 'r') as f:
        return json.load(f)

# حفظ المفاتيح في ملف JSON
def save_keys(keys):
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

# التحقق من صلاحية المفتاح
def validate_api_key(api_key):
    keys = load_keys()
    if api_key in keys.values():
        return True
    abort(403, description="Invalid API Key")

@app.route("/", methods=["GET"])
def read_root():
    return jsonify({"message": "API is working"})

@app.route("/check-key/<key_name>", methods=["GET"])
def check_key(key_name):
    api_key = request.headers.get(API_KEY_NAME)
    validate_api_key(api_key)

    keys = load_keys()
    if key_name in keys:
        return jsonify({"key": key_name, "value": keys[key_name], "status": "valid"})
    abort(404, description="Key not found")

@app.route("/add-key/<key_name>/<key_value>", methods=["POST"])
def add_key(key_name, key_value):
    api_key = request.headers.get(API_KEY_NAME)
    validate_api_key(api_key)

    keys = load_keys()
    keys[key_name] = key_value
    save_keys(keys)
    return jsonify({"status": "success", "message": f"Key {key_name} added"})

@app.route("/remove-key/<key_name>", methods=["DELETE"])
def remove_key(key_name):
    api_key = request.headers.get(API_KEY_NAME)
    validate_api_key(api_key)

    keys = load_keys()
    if key_name in keys:
        del keys[key_name]
        save_keys(keys)
        return jsonify({"status": "success", "message": f"Key {key_name} removed"})
    abort(404, description="Key not found")

if __name__ == "__main__":
    app.run()
