from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import json
import os

app = FastAPI()

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

KEYS_FILE = "kys.json"

def load_keys():
    if not os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, 'w') as f:
            json.dump({}, f)
    with open(KEYS_FILE, 'r') as f:
        return json.load(f)

def save_keys(keys):
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

async def validate_api_key(api_key: str = Security(api_key_header)):
    keys = load_keys()
    if api_key in keys.values():
        return True
    raise HTTPException(status_code=403, detail="Invalid API Key")

@app.get("/")
async def read_root():
    return {"message": "API is working"}

@app.get("/check-key/{key_name}")
async def check_key(key_name: str, is_valid: bool = Security(validate_api_key)):
    keys = load_keys()
    if key_name in keys:
        return {"key": key_name, "value": keys[key_name], "status": "valid"}
    raise HTTPException(status_code=404, detail="Key not found")

@app.post("/add-key/{key_name}/{key_value}")
async def add_key(key_name: str, key_value: str, is_valid: bool = Security(validate_api_key)):
    keys = load_keys()
    keys[key_name] = key_value
    save_keys(keys)
    return {"status": "success", "message": f"Key {key_name} added"}

@app.delete("/remove-key/{key_name}")
async def remove_key(key_name: str, is_valid: bool = Security(validate_api_key)):
    keys = load_keys()
    if key_name in keys:
        del keys[key_name]
        save_keys(keys)
        return {"status": "success", "message": f"Key {key_name} removed"}
    raise HTTPException(status_code=404, detail="Key not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run()
