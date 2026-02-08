# Deployment Information

## Server Details
- **VPS IP:** 
- **Domain:** https://thunnwathanlin.tech
- **OS:** Ubuntu 22.04.5 LTS
- **Python:** 3.10+
- **Django:** Latest
- **Web Server:** Nginx + Gunicorn

## Services
- **Django App:** `mysite.service` (port 8001)
- **Web Server:** `nginx.service` (ports 80, 443)
- **Auto-start:** Enabled (survives reboot)

## File Locations
- **Application:** `/opt/mysite/`
- **Virtual Environment:** `/opt/mysite/.venv/`
- **Database:** `/opt/mysite/db.sqlite3`
- **Media Files:** `/opt/mysite/media/`
- **Static Files:** `/opt/mysite/staticfiles/`
- **Templates:** `/opt/mysite/templates/`

## Configuration Files
- **Nginx:** `/etc/nginx/sites-available/mysite`
- **Gunicorn Service:** `/etc/systemd/system/mysite.service`
- **Upload Limits:** `/etc/nginx/conf.d/upload_limit.conf`

## Important Settings
- **Max Upload:** 700 MB
- **Timeout:** 300 seconds (5 minutes)
- **Workers:** 2 Gunicorn workers
- **SSL:** Let's Encrypt (auto-renewal)

## Management Commands

### Service Management
```bash
# Restart Django app
systemctl restart mysite.service

# Restart Nginx
systemctl reload nginx

# View logs
journalctl -u mysite.service -f

# Check status
systemctl status mysite.service nginx
```

### Django Management
```bash
cd /opt/mysite
source .venv/bin/activate

# Run migrations
python3 manage.py migrate

# Create superuser
python3 manage.py createsuperuser

# Collect static files
python3 manage.py collectstatic
```

### Git Operations
```bash
cd /opt/mysite
git pull origin main
systemctl restart mysite.service
```

## Features
- ✅ Admin panel with role-based permissions (Superadmin, Editor)
- ✅ User management interface
- ✅ Post management with cover images
- ✅ Media library (audio/video with tracks)
- ✅ Markdown support with preview
- ✅ Dark theme design
- ✅ Responsive layout (mobile + desktop)
- ✅ Large file uploads (700 MB)
- ✅ Auto-start on reboot

## User Roles
- **Superadmin:** Full access (create, edit, delete, manage users)
- **Editor:** Create and edit posts only (no delete, no user management)

## Backup Recommendations
1. Database: `/opt/mysite/db.sqlite3`
2. Media files: `/opt/mysite/media/`
3. Configuration: Copy service files and nginx config

## GitHub Repository
- **URL:** https://github.com/yannaing86tt/website
- **Branch:** main
- **Contains:** Code, templates, installation scripts (NO database/media)

## One-Click Install (Fresh VPS)
```bash
curl -sSL https://raw.githubusercontent.com/yannaing86tt/website/main/install.sh | bash
```

## Notes
- Database and media files are NOT in GitHub repository
- Posts and user accounts exist only on the VPS
- Fresh install creates empty database
- Services auto-start on VPS reboot
- SSL certificate auto-renews via certbot

---

**Last Updated:** February 8, 2026
