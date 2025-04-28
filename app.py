from flask import Flask, jsonify
import json
import asyncio
import aiohttp

app = Flask(__name__)

# بيانات Cloudinary
CLOUDINARY_CLOUD_NAME = "duu2fy7bq"

# تنزيل الملف من Cloudinary (غير متزامن)
async def download_file_from_cloudinary():
    url = f"https://res.cloudinary.com/{CLOUDINARY_CLOUD_NAME}/raw/upload/v1/keys/ky.txt"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    file_content = await response.text()
                    return file_content
                else:
                    raise Exception("Failed to download file from Cloudinary")
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

# نقطة النهاية لعرض المفاتيح
@app.route('/keys', methods=['GET'])
async def get_keys():
    file_content = await download_file_from_cloudinary()
    if not file_content:
        return jsonify({"status": "error", "message": "Failed to fetch keys"}), 500

    # تحويل المحتوى إلى قاموس
    keys = {}
    for line in file_content.splitlines():
        if "=" in line:
            key_name, key_value = line.split("=")
            keys[key_name.strip()] = key_value.strip().strip('"')

    return jsonify({"status": "success", "keys": keys})

# تشغيل التطبيق
if __name__ == "__main__":
    app.run(debug=True)
