# Railway License Admin

Simple license server + admin UI untuk aplikasi ScrapUserAgent.

## Cara pakai (lokal)
1. Salin `.env.example` -> `.env` dan set `ADMIN_TOKEN`.
2. Install deps: `pip install -r requirements.txt`
3. Jalankan: `uvicorn app:app --host 0.0.0.0 --port 8000`
4. Buka `admin/index.html` di browser dan masukkan token.

## Deploy ke Railway
- Buat repo GitHub dan push repo ini.
- Di Railway: New Project -> Deploy from GitHub -> pilih branch.
- Set env var `ADMIN_TOKEN` pada Railway ke token kuat.
- Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

## Menghubungkan client (ScrapUserAgent)
- Update `LICENSE_SERVER` di `main.py` (program kamu) jadi URL Railway kamu.
