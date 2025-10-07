#!/bin/bash
# ===============================
# 🚀 Auto Deploy ke GitHub + Railway
# Project: railway_license_admin
# Author: akubsaputra
# ===============================

REPO_URL="https://github.com/akubsaputra/railway_license_admin.git"
BRANCH="main"

echo ""
echo "🧩 Menyimpan perubahan lokal..."
git add .
git commit -m "update $(date '+%Y-%m-%d %H:%M:%S')" || echo "Tidak ada perubahan untuk di-commit."

echo ""
echo "📤 Push ke GitHub ($BRANCH)..."
git branch -M $BRANCH
git push -u origin $BRANCH

if [ $? -ne 0 ]; then
  echo "❌ Push ke GitHub gagal. Cek koneksi internet atau token akses GitHub kamu."
  exit 1
fi

echo ""
echo "⏳ Menunggu Railway memproses redeploy..."
sleep 3

# Optional: Trigger redeploy otomatis via Railway CLI (jika sudah login)
if command -v railway &> /dev/null
then
  echo "🚀 Menjalankan redeploy via Railway CLI..."
  railway redeploy || echo "⚠️ Gagal trigger via CLI, lakukan redeploy manual di dashboard Railway."
else
  echo "⚙️ Railway CLI belum terinstal. Jalankan manual di:"
  echo "👉 https://railway.app/project"
fi

echo ""
echo "✅ Selesai! Cek hasilnya di:"
echo "👉 https://railway_license_admin.railway.app/admin/"
