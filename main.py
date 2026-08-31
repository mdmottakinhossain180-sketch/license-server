from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# লাইসেন্স কন্ট্রোল ডাটাবেজ
LICENSES = {
    "MOTTAKIN-VIP-101": {
        "max_devices": 2,          # সর্বোচ্চ ২ টি ডিভাইসে চলবে
        "expiry_date": "2026-10-31", # মেয়াদ (YYYY-MM-DD)
        "allowed_hwids": []         # অটোমেটিক প্রথম ২টি ডিভাইস সেভ হবে
    },
    "CLIENT-1-MONTH": {
        "max_devices": 1,          # ১ টি ডিভাইসে চলবে
        "expiry_date": "2026-09-30", # ১ মাসের মেয়াদ
        "allowed_hwids": []
    }
}

class LicenseRequest(BaseModel):
    license_key: str
    hwid: str

@app.get("/")
def home():
    return {"status": "Server active"}

@app.post("/verify")
def verify_license(req: LicenseRequest):
    key_info = LICENSES.get(req.license_key)
    
    if not key_info:
        return {"status": "error", "message": "অবৈধ লাইসেন্স কী!"}
    
    # ১. মেয়াদ চেক
    today = datetime.now().strftime("%Y-%m-%d")
    if today > key_info["expiry_date"]:
        return {"status": "error", "message": "লাইসেন্স মেয়াউত্তীর্ণ হয়ে গেছে!"}
    
    # ২. ডিভাইস লিমিট ও HWID চেক
    hwids = key_info["allowed_hwids"]
    if req.hwid in hwids:
        return {"status": "success", "message": "লাইসেন্স ভ্যালিড!"}
    
    if len(hwids) < key_info["max_devices"]:
        hwids.append(req.hwid) # নতুন ডিভাইস সেভ হলো
        return {"status": "success", "message": "নতুন ডিভাইসে অ্যাক্টিভেট হয়েছে!"}
    
    return {"status": "error", "message": "ডিভাইস লিমিট পার হয়ে গেছে!"}
    
