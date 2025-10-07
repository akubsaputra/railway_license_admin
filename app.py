<<<<<<< HEAD
=======

>>>>>>> f886b0369e20258d1bd0e379e5edca5ed2b74a88
import os
import json
import hashlib
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict

DB_FILE = os.getenv("DB_FILE", "users.json")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "changeme-admin-token")

app = FastAPI(title="License Server - ScrapUserAgent")
security = HTTPBearer()

def load_users() -> Dict:
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_users(data: Dict):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

class LoginReq(BaseModel):
    username: str
    password: str
    device: str = ""

class AddUserReq(BaseModel):
    username: str
    password: str
    device: str = ""

@app.post("/login")
async def login(req: LoginReq):
    users = load_users()
    u = users.get(req.username)
    if not u:
        return JSONResponse({"status": "fail", "message": "Invalid login"}, status_code=401)
    if u.get("password") != hash_pw(req.password):
        return JSONResponse({"status": "fail", "message": "Invalid login"}, status_code=401)
    u["device"] = req.device
    users[req.username] = u
    save_users(users)
    return {"status": "ok", "message": "Login success"}

def admin_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid admin token")
    return True

@app.get("/admin/users")
async def list_users(authed: bool = Depends(admin_auth)):
    return load_users()

@app.post("/admin/add")
async def add_user(req: AddUserReq, authed: bool = Depends(admin_auth)):
    users = load_users()
    if req.username in users:
        return JSONResponse({"status": "fail", "message": "User exists"}, status_code=400)
    users[req.username] = {"password": hash_pw(req.password), "device": req.device}
    save_users(users)
    return {"status": "ok", "message": "User added"}

@app.post("/admin/remove")
async def remove_user(req: Request, authed: bool = Depends(admin_auth)):
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
<<<<<<< HEAD
=======
from fastapi.staticfiles import StaticFiles
app.mount("/admin", StaticFiles(directory="admin", html=True), name="admin")
>>>>>>> f886b0369e20258d1bd0e379e5edca5ed2b74a88
from fastapi.staticfiles import StaticFiles
import os

# ✅ Aman: hanya mount kalau folder 'admin' benar-benar ada
if os.path.exists("admin"):
    app.mount("/admin", StaticFiles(directory="admin", html=True), name="admin")
    print("✅ Folder 'admin' ditemukan — Admin Panel aktif di /admin/")
else:
    print("⚠️ Folder 'admin' tidak ditemukan — Admin Panel tidak dilayani.")

@app.get("/health")
async def health():
    return {"status": "ok"}
