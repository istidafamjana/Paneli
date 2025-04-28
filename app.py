from flask import Flask, jsonify, request, abort
import json
import os
from functools import wraps

app = Flask(__name__)

# مسار ملف المفاتيح
KEYS_FILE = os.path.join(os.path.dirname(__file__), '..', 'kys.json')

def load_keys():
    """تحميل المفاتيح من ملف JSON"""
    if not os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, 'w') as f:
            json.dump({}, f)
    with open(KEYS_FILE, 'r') as f:
        return json.load(f)

def save_keys(keys):
    """حفظ المفاتيح إلى ملف JSON"""
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

def require_api_key(view_function):
    """ديكوراتور للتحقق من صحة مفتاح API"""
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        keys = load_keys()
        
        if api_key in keys.values():
            return view_function(*args, **kwargs)
        else:
            abort(403, description="Invalid API Key")
    return decorated_function

@app.route('/')
def home():
    return jsonify({"status": "running", "message": "Welcome to Keys API"})

@app.route('/check-key/<key_name>', methods=['GET'])
@require_api_key
def check_key(key_name):
    keys = load_keys()
    if key_name in keys:
        return jsonify({
            "status": "success",
            "key": key_name,
            "value": keys[key_name]
        })
    else:
        abort(404, description="Key not found")

@app.route('/add-key', methods=['GET'])
@require_api_key
def add_key():
    # استخراج المعلمات من Query Parameters
    key_name = request.args.get('key_name')
    key_value = request.args.get('key_value')
    
    if not key_name or not key_value:
        abort(400, description="Both key_name and key_value are required")
    
    keys = load_keys()
    keys[key_name] = key_value
    save_keys(keys)
    return jsonify({
        "status": "success",
        "message": f"Key {key_name} added",
        "key": key_name,
        "value": key_value
    })

@app.route('/remove-key/<key_name>', methods=['DELETE'])
@require_api_key
def remove_key(key_name):
    keys = load_keys()
    if key_name in keys:
        del keys[key_name]
        save_keys(keys)
        return jsonify({
            "status": "success",
            "message": f"Key {key_name} removed"
        })
    else:
        abort(404, description="Key not found")

@app.errorhandler(400)
@app.errorhandler(403)
@app.errorhandler(404)
def handle_error(e):
    return jsonify({
        "status": "error",
        "code": e.code,
        "message": e.description
    }), e.code

# هذا مهم لتشغيل التطبيق على Vercel
if __name__ == '__main__':
    app.run()
