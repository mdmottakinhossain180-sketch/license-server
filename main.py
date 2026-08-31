from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()

# লাইসেন্স ডাটাবেজ
LICENSES = {
    # ------------------ ১ মাসের লাইসেন্স (১০টি) ------------------
    "MOTTAKIN-1M-01": {"type": "1M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-1M-02": {"type": "1M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-1M-03": {"type": "1M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-1M-04": {"type": "1M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-1M-05": {"type": "1M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-1M-06": {"type": "1M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-1M-07": {"type": "1M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-1M-08": {"type": "1M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-1M-09": {"type": "1M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-1M-10": {"type": "1M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},

    # ------------------ ২ মাসের লাইসেন্স (১০টি) ------------------
    "MOTTAKIN-2M-01": {"type": "2M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-2M-02": {"type": "2M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-2M-03": {"type": "2M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-2M-04": {"type": "2M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-2M-05": {"type": "2M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-2M-06": {"type": "2M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-2M-07": {"type": "2M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-2M-08": {"type": "2M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-2M-09": {"type": "2M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},
    "MOTTAKIN-2M-10": {"type": "2M", "max_devices": 2, "activated_at": None, "allowed_hwids": []},

    # ------------------ লাইফটাইম লাইসেন্স ------------------
    "MOTTAKIN-LIFETIME-VIP": {"type": "LIFETIME", "max_devices": "UNLIMITED", "activated_at": None, "allowed_hwids": []}
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
    
    # ১. লাইফটাইম চেক
    if key_info["type"] == "LIFETIME":
        return {"status": "success", "message": "লাইফটাইম আনলিমিটেড অ্যাক্সেস ভ্যালিড!"}
    
    now = datetime.now()

    # ২. ডাইনামিক অ্যাক্টিভেশন
    if key_info["activated_at"] is None:
        key_info["activated_at"] = now
    
    days_limit = 30 if key_info["type"] == "1M" else 60
    expiry_date = key_info["activated_at"] + timedelta(days=days_limit)
    exp_str = expiry_date.strftime("%Y-%m-%d")
    
    if now > expiry_date:
        return {"status": "error", "message": "লাইসেন্স মেয়াউত্তীর্ণ হয়ে গেছে!"}

    # ৩. HWID ডিভাইস লকিং (সর্বোচ্চ ২টি ডিভাইস)
    hwids = key_info["allowed_hwids"]
    
    if req.hwid in hwids:
        return {"status": "success", "message": "লাইসেন্স ভ্যালিড! মেয়াদ শেষ হবে: " + exp_str}
    
    if len(hwids) < key_info["max_devices"]:
        hwids.append(req.hwid)
        return {"status": "success", "message": "নতুন ডিভাইসে এক্টিভেট হয়েছে! মেয়াদ শেষ হবে: " + exp_str}
    
    return {"status": "error", "message": "সর্বোচ্চ সংখ্যক ডিভাইসে লগইন করা হয়ে গেছে!"}
