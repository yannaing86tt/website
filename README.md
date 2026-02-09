# Django Website - One-Click Installer

Automated installation script for deploying a Django-based website with Nginx, Gunicorn, and SSL.

## Features

- ✅ Automated system setup
- ✅ Python 3 + Virtual environment
- ✅ Django + Gunicorn
- ✅ Nginx reverse proxy
- ✅ SSL certificate (Let's Encrypt)
- ✅ Media file handling (up to 700 MB)
- ✅ Database migrations
- ✅ Admin user creation
- ✅ Customizable site name and branding
- ✅ Optional Telegram/Facebook links

## Requirements

- Fresh Ubuntu 22.04+ VPS
- Root access
- Domain name pointed to your server IP (A record)
- At least 1GB RAM

## Quick Install

**⚠️ Important:** Use the wget method to avoid GitHub cache issues:

```bash
wget https://raw.githubusercontent.com/yannaing86tt/website/main/install.sh -O /tmp/install.sh
bash /tmp/install.sh
```

**Alternative (may use cached version):**
```bash
curl -sSL https://raw.githubusercontent.com/yannaing86tt/website/main/install.sh | bash
```

## Installation Prompts

The script will ask you for:

1. **Domain name** (e.g., example.com)
2. **Website name** (displayed in header and title)
3. **Footer name** (copyright owner name)
4. **Telegram channel URL** (optional - press Enter to skip)
5. **Facebook page URL** (optional - press Enter to skip)
6. **Admin username**
7. **Admin password**
8. **Admin email**

### Example:
```
Domain name: example.com
Website name: My Tech Blog
Footer name: John Doe
Telegram URL: https://t.me/mychannel (or press Enter)
Facebook URL: https://facebook.com/mypage (or press Enter)
Admin username: admin
Admin password: ********
Admin email: admin@example.com
```

## What Gets Installed

- Python 3.12 + pip + venv + dev tools
- Nginx web server
- Certbot (SSL certificates)
- Build tools (gcc, make, etc.)
- Git
- All Python dependencies from `requirements.txt`
- Gunicorn WSGI server
- SQLite database

## Post-Installation

After installation completes:

1. Visit `https://yourdomain.com` to see your website
2. Access admin panel at `https://yourdomain.com/panel`
3. Login with the credentials you provided

## File Locations

- **Website code:** `/opt/mysite`
- **Media files:** `/opt/mysite/media`
- **Static files:** `/opt/mysite/staticfiles`
- **Environment:** `/opt/mysite/.env`
- **Database:** `/opt/mysite/db.sqlite3`
- **Service:** `/etc/systemd/system/mysite.service`
- **Nginx config:** `/etc/nginx/sites-available/mysite`

## Managing the Site

### Restart website
```bash
systemctl restart mysite.service
```

### View logs
```bash
journalctl -u mysite.service -f
```

### Reload Nginx
```bash
systemctl reload nginx
```

### Edit environment variables
```bash
nano /opt/mysite/.env
systemctl restart mysite.service
```

## Upload Limits

- **Max file size:** 700 MB
- **Timeout:** 5 minutes per upload

## Complete Cleanup

To remove everything and start fresh:

```bash
# Stop services
systemctl stop mysite.service nginx

# Remove service
systemctl disable mysite.service
rm -f /etc/systemd/system/mysite.service
systemctl daemon-reload

# Remove files
rm -rf /opt/mysite

# Remove software
apt-get purge -y nginx nginx-common certbot python3-certbot-nginx python3-pip python3-venv python3-dev build-essential git
rm -rf /etc/nginx /etc/letsencrypt

# Clean up
apt-get autoremove -y
apt-get autoclean -y
```

## Troubleshooting

### Installation fails with "username must be set"
- Make sure you enter all required fields (don't leave them empty)
- Use the wget method instead of curl

### SSL certificate fails
- Verify DNS records are pointing to your server
- Check firewall allows ports 80 and 443
- Run manually: `certbot --nginx -d yourdomain.com`

### Website shows 500 error
- Check logs: `journalctl -u mysite.service -n 50`
- Verify database permissions: `ls -la /opt/mysite/db.sqlite3`
- Restart service: `systemctl restart mysite.service`

## Customization

The following can be customized during installation:
- Website name (appears in header, title, footer)
- Footer copyright name
- Telegram channel link (optional)
- Facebook page link (optional)

All settings are stored in `/opt/mysite/.env` and can be changed after installation.

## Support

For issues or questions, open an issue on GitHub.

## License

MIT License
