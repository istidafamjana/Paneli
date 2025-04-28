from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

# بيانات Cloudinary (استبدل هذه القيم بمعلومات حسابك)
CLOUDINARY_CLOUD_NAME = "duu2fy7bq"
CLOUDINARY_API_KEY = "459654532934462"  # استبدل بمفتاح API الخاص بك
CLOUDINARY_API_SECRET = "WMWrndmiqcot_20p0rc50odjPTw"  # استبدل بالسر الخاص بك
CLOUDINARY_URL = f"https://res.cloudinary.com/{CLOUDINARY_CLOUD_NAME}/raw/upload/v1/keys/ky.txt"

# تنزيل الملف من Cloudinary
def download_file_from_cloudinary():
    try:
        response = requests.get(CLOUDINARY_URL)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception("Failed to download file from Cloudinary")
    except Exception as e:
        print(f"Error downloading file: {e}")
        return {}

# رفع الملف إلى Cloudinary
def upload_file_to_cloudinary(data):
    upload_url = f"https://api.cloudinary.com/v1_1/{CLOUDINARY_CLOUD_NAME}/raw/upload"
    files = {
        "file": ("ky.txt", json.dumps(data), "application/json"),
        "upload_preset": "your_upload_preset"  # استبدل بـ upload preset الخاص بك
    }
    headers = {
        "Authorization": f"Basic {CLOUDINARY_API_KEY}:{CLOUDINARY_API_SECRET}"
    }
    response = requests.post(upload_url, files=files, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to upload file to Cloudinary")

# نقطة النهاية لعرض المفاتيح
@app.route('/keys', methods=['GET'])
def get_keys():
    keys = download_file_from_cloudinary()
    return jsonify(keys)

# تشغيل التطبيق
if __name__ == "__main__":
    app.run(debug=True)
