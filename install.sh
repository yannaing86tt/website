#!/bin/bash
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Django Website Installer${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script must be run as root${NC}"
   exit 1
fi

# Update system
echo -e "${YELLOW}[1/12] Updating system...${NC}"
apt-get update -qq

# Install dependencies
echo -e "${YELLOW}[2/12] Installing dependencies...${NC}"
apt-get install -y -qq python3 python3-pip python3-venv python3-dev build-essential git curl certbot
# Install nginx separately and stop it immediately
apt-get install -y -qq nginx
systemctl stop nginx
apt-get install -y -qq python3-certbot-nginx

# Collect information
echo ""
echo -e "${GREEN}Please provide the following information:${NC}"
echo ""

# Use -r flag to prevent backslash escapes and handle input properly
read -r -p "Domain name (e.g., example.com): " DOMAIN
read -r -p "Website name: " SITE_NAME
read -r -p "Footer name (copyright owner): " FOOTER_NAME
read -r -p "Telegram channel URL (optional, press Enter to skip): " TELEGRAM_URL
read -r -p "Facebook page URL (optional, press Enter to skip): " FACEBOOK_URL
read -r -p "Admin username: " ADMIN_USER
read -r -s -p "Admin password: " ADMIN_PASS
echo ""
read -r -p "Admin email: " ADMIN_EMAIL

# Strip control characters and validate inputs
DOMAIN=$(echo "$DOMAIN" | tr -d '[:cntrl:]' | tr -cd '[:alnum:].-')
SITE_NAME=$(echo "$SITE_NAME" | tr -d '[:cntrl:]')
FOOTER_NAME=$(echo "$FOOTER_NAME" | tr -d '[:cntrl:]')
TELEGRAM_URL=$(echo "$TELEGRAM_URL" | tr -d '[:cntrl:]')
FACEBOOK_URL=$(echo "$FACEBOOK_URL" | tr -d '[:cntrl:]')
ADMIN_USER=$(echo "$ADMIN_USER" | tr -d '[:cntrl:]' | tr -cd '[:alnum:]_-')
ADMIN_EMAIL=$(echo "$ADMIN_EMAIL" | tr -d '[:cntrl:]')

# Validate required fields
if [ -z "$DOMAIN" ]; then
    echo -e "${RED}Error: Domain name is required${NC}"
    exit 1
fi

if [ -z "$ADMIN_USER" ]; then
    echo -e "${RED}Error: Admin username is required${NC}"
    exit 1
fi

if [ -z "$ADMIN_PASS" ]; then
    echo -e "${RED}Error: Admin password is required${NC}"
    exit 1
fi

# Generate secret key using openssl (remove newlines)
SECRET_KEY=$(openssl rand -base64 50 | tr -d "\n=+/" | cut -c1-50)

# Set installation directory
INSTALL_DIR="/opt/mysite"
REPO_URL="https://github.com/yannaing86tt/website.git"

# Clone repository
echo -e "${YELLOW}[3/12] Cloning repository...${NC}"
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
fi
git clone "$REPO_URL" "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Create virtual environment
echo -e "${YELLOW}[4/12] Creating virtual environment...${NC}"
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
echo -e "${YELLOW}[5/12] Installing Python packages...${NC}"
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Create .env file
echo -e "${YELLOW}[6/12] Configuring environment...${NC}"
cat > .env << ENVFILE
DJANGO_SECRET_KEY=$SECRET_KEY
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN
SITE_NAME=$SITE_NAME
SITE_URL=https://$DOMAIN
FOOTER_NAME=$FOOTER_NAME
TELEGRAM_URL=$TELEGRAM_URL
FACEBOOK_URL=$FACEBOOK_URL
ENVFILE

# Create media directories
echo -e "${YELLOW}[7/12] Creating media directories...${NC}"
mkdir -p media/covers media/library media/library_covers media/library_tracks
chown -R www-data:www-data media
chmod -R 755 media

# Run migrations
echo -e "${YELLOW}[8/12] Running database migrations...${NC}"
python3 manage.py migrate --noinput

# Create superuser
echo -e "${YELLOW}[9/12] Creating admin user...${NC}"
python3 manage.py shell << PYEOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$ADMIN_USER').exists():
    User.objects.create_superuser('$ADMIN_USER', '$ADMIN_EMAIL', '$ADMIN_PASS')
PYEOF

# Collect static files
python3 manage.py collectstatic --noinput

# Fix database permissions for SQLite
chown www-data:www-data db.sqlite3
chmod 664 db.sqlite3
chown www-data:www-data .
chmod 775 .

# Create Gunicorn service
echo -e "${YELLOW}[10/12] Setting up Gunicorn service...${NC}"
cat > /etc/systemd/system/mysite.service << SERVICEEOF
[Unit]
Description=mysite gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$INSTALL_DIR
EnvironmentFile=$INSTALL_DIR/.env
Environment="DJANGO_SETTINGS_MODULE=config.settings"

ExecStart=$INSTALL_DIR/.venv/bin/gunicorn \\
  --chdir $INSTALL_DIR \\
  config.wsgi:application \\
  --bind 127.0.0.1:8001 \\
  --workers 2 \\
  --timeout 300

Restart=always

[Install]
WantedBy=multi-user.target
SERVICEEOF

# Enable and start service
systemctl daemon-reload
systemctl enable mysite.service
systemctl start mysite.service

# Configure Nginx
echo -e "${YELLOW}[11/12] Configuring Nginx...${NC}"
# Ensure directories exist
mkdir -p /etc/nginx/sites-available
mkdir -p /etc/nginx/sites-enabled

cat > /etc/nginx/sites-available/mysite << NGINXEOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    client_max_body_size 700M;

    location /static/ {
        alias $INSTALL_DIR/staticfiles/;
        access_log off;
        expires 30d;
    }

    location /media/ {
        alias $INSTALL_DIR/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
}
NGINXEOF

# Enable site and remove default
rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/
nginx -t
systemctl start nginx

# Configure firewall
echo -e "${YELLOW}Configuring firewall...${NC}"
if command -v ufw &> /dev/null; then
    ufw allow 80/tcp
    ufw allow 443/tcp
    echo -e "${GREEN}Firewall configured (ports 80, 443)${NC}"
fi

# Configure SSL
echo -e "${YELLOW}[12/12] Configuring SSL certificate...${NC}"
certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --register-unsafely-without-email || {
    echo -e "${YELLOW}SSL certificate setup failed. You can run it manually later:${NC}"
    echo -e "certbot --nginx -d $DOMAIN -d www.$DOMAIN"
}

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "Website: ${GREEN}https://$DOMAIN${NC}"
echo -e "Admin Panel: ${GREEN}https://$DOMAIN/panel/${NC}"
echo -e "Admin Login: ${GREEN}$ADMIN_USER${NC}"
echo ""
echo -e "${YELLOW}Note: If SSL setup failed, run manually:${NC}"
echo -e "certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo ""
