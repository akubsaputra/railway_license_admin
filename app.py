import os
import json
import hashlib
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict

# =============== Config ===============
DB_FILE = os.getenv("DB_FILE", "users.json")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "changeme-admin-token")

app = FastAPI(title="License Server - ScrapUserAgent")
security = HTTPBearer()

# =============== Helper Functions ===============

def load_users() -> Dict:
    """Load user data from JSON file."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Gagal load users.json: {e}")
            return {}
    return {}

def save_users(data: Dict):
    """Save user data to JSON file."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def hash_pw(pw: str) -> str:
    """SHA-256 password hashing."""
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

# =============== Models ===============

class LoginReq(BaseModel):
    username: str
    password: str
    device: str = ""

class AddUserReq(BaseModel):
    username: str
    password: str
    device: str = ""

# =============== Public API ===============

@app.post("/login")
async def login(req: LoginReq):
    """Endpoint untuk user login."""
    users = load_users()
    u = users.get(req.username)
    if not u or u.get("password") != hash_pw(req.password):
        return JSONResponse({"status": "fail", "message": "Invalid login"}, status_code=401)

    # Update device info
    u["device"] = req.device
    users[req.username] = u
    save_users(users)
    return {"status": "ok", "message": "Login success"}

# =============== Admin Authentication ===============

def admin_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Simple token-based admin auth."""
    token = credentials.credentials
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid admin token")
    return True

# =============== Admin API ===============

@app.get("/admin/users")
async def list_users(authed: bool = Depends(admin_auth)):
    """List all users."""
    return load_users()

@app.post("/admin/add")
async def add_user(req: AddUserReq, authed: bool = Depends(admin_auth)):
    """Add new user."""
    users = load_users()
    if req.username in users:
        return JSONResponse({"status": "fail", "message": "User exists"}, status_code=400)
    users[req.username] = {"password": hash_pw(req.password), "device": req.device}
    save_users(users)
    return {"status": "ok", "message": "User added"}

@app.post("/admin/remove")
async def remove_user(req: Request, authed: bool = Depends(admin_auth)):
    """Remove user."""
    body = await req.json()
    username = body.get("username")
    if not username:
        return JSONResponse({"status": "fail", "message": "Missing username"}, status_code=400)
    users = load_users()
    if username not in users:
        return JSONResponse({"status": "fail", "message": "User not found"}, status_code=404)
    users.pop(username)
    save_users(users)
    return {"status": "ok", "message": "User removed"}

# =============== Static Admin Panel (Absolute Path + Fallback) ===============

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADMIN_DIR = os.path.join(BASE_DIR, "admin")

if os.path.exists(ADMIN_DIR):
    files = os.listdir(ADMIN_DIR)
    print(f"✅ Folder 'admin' ditemukan ({len(files)} file): {', '.join(files)}")

    # Serve static files from absolute path
    app.mount("/admin", StaticFiles(directory=ADMIN_DIR, html=True), name="admin")

    # ✅ Redirect /admin → /admin/
    @app.get("/admin", include_in_schema=False)
    async def admin_redirect():
        return RedirectResponse(url="/admin/")

    # ✅ Serve index.html at /admin/
    @app.get("/admin/", include_in_schema=False)
    async def admin_root():
        return FileResponse(os.path.join(ADMIN_DIR, "index.html"))

else:
    print("⚠️ Folder 'admin' tidak ditemukan — Admin Panel tidak dilayani.")

# =============== Health Check ===============

@app.get("/health")
async def health():
    """Cek status server."""
    return {"status": "ok"}
