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

## Requirements

- Fresh Ubuntu 22.04/20.04 or Debian 11/12 VPS
- Root access
- Domain name pointed to your server IP (A record)

## Quick Install

Run this command as root:

```bash
curl -sSL https://raw.githubusercontent.com/yannaing86tt/website/main/install.sh | bash
```

Or with wget:

```bash
wget -qO- https://raw.githubusercontent.com/yannaing86tt/website/main/install.sh | bash
```

## Installation Prompts

The script will ask you for:

1. **Domain name** (e.g., example.com)
2. **Website name** (displayed on site)
3. **Admin username**
4. **Admin password**
5. **Admin email**

## What Gets Installed

- Python 3 + pip + venv
- Nginx web server
- Certbot (SSL certificates)
- All Python dependencies from `requirements.txt`
- Gunicorn WSGI server
- Database (SQLite by default)

## Post-Installation

After installation completes:

1. Visit `https://yourdomain.com` to see your website
2. Access admin panel at `https://yourdomain.com/admin`
3. Login with the credentials you provided

## File Locations

- **Website code:** `/opt/mysite`
- **Media files:** `/opt/mysite/media`
- **Static files:** `/opt/mysite/staticfiles`
- **Logs:** `journalctl -u mysite.service`

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

## Upload Limits

- **Max file size:** 700 MB
- **Timeout:** 5 minutes per upload

## Support

For issues or questions, contact the repository maintainer.

## License

MIT License
