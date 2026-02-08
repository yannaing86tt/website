# New Website (Django) – One-Line VPS Installer

ဒီ project က **Django-based website + admin panel** ကို  
**VPS အသစ် + domain အသစ်** မှာ **one-line installer script** နဲ့ အလွယ်တကူ deploy လုပ်နိုင်အောင် ပြုလုပ်ထားပါတယ်။

👉 အဟောင်း website ထဲက **posts / media / database contents မပါဘဲ**  
👉 **code + UI + panel structure** ပဲ clean install လုပ်ပေးပါတယ်

---

## ✨ Features

- Django website (public pages + admin panel)
- PostgreSQL database (empty DB – no old posts)
- Nginx + Gunicorn
- Let’s Encrypt SSL (HTTPS auto)
- `.env` based configuration
- One-line installer (interactive prompts)
- Mobile friendly UI + custom admin panel
- Media upload support (mp3 multi-upload ready)

---

## 📦 What this installer does

Installer script က run လိုက်တာနဲ့ အောက်ပါအလုပ်တွေကို **အလိုအလျောက်** လုပ်ပေးပါတယ်—

- VPS system packages install
- GitHub repo clone
- Python venv setup + requirements install
- `.env` auto generate
- PostgreSQL DB + user create (empty DB)
- Django migrate + superuser create
- collectstatic
- Gunicorn systemd service
- Nginx config
- Let’s Encrypt SSL (HTTPS)
- Firewall (UFW) basic rules

---

## 🖥 Requirements

- **Fresh VPS** (Ubuntu 22.04 / 24.04 recommended)
- **Root access**
- **Domain name** (DNS A record → VPS IP)
- Ports **80 / 443** open

---

## 🚀 One-Line Installation

VPS အသစ်ထဲမှာ ဒီ command ကိုပဲ run လုပ်ပါ👇

```bash
curl -fsSL https://raw.githubusercontent.com/yannaing86tt/new_website/main/install.sh | sudo bash
```
