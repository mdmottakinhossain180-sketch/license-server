from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# আপনার অনুমোদিত ক্লায়েন্টদের লাইসেন্স কি
LICENSES = {
    "MOTTAKIN-VIP-101": "PENDING",
    "CLIENT-KEY-2026": "PENDING"
}

class VerifyRequest(BaseModel):
    license_key: str
    hwid: str

@app.get("/")
def home():
    return {"status": "Server active"}

@app.post("/verify")
def verify(data: VerifyRequest):
    key = data.license_key
    hwid = data.hwid
    
    if key not in LICENSES:
        raise HTTPException(status_code=401, detail="Invalid License Key!")
    
    if LICENSES[key] == "PENDING":
        LICENSES[key] = hwid
        return {"status": "success", "message": "License bound successfully!"}
    
    if LICENSES[key] == hwid:
        return {"status": "success", "message": "Access Granted!"}
    else:
        raise HTTPException(status_code=403, detail="Device Mismatch!")
      
