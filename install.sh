#!/usr/bin/env bash
set -euo pipefail

# ========= helpers =========
die(){ echo "❌ $*" >&2; exit 1; }
ok(){ echo "✅ $*"; }
info(){ echo "ℹ️  $*"; }

need_root(){
  [[ "${EUID:-999}" -eq 0 ]] || die "Run as root: sudo -i"
}

read_tty(){ # var prompt secret(0/1) default(optional)
  local __var="$1" __msg="$2" __secret="${3:-0}" __def="${4:-}"
  local val=""
  if [[ "$__secret" == "1" ]]; then
    read -r -s -p "$__msg: " val; echo
  else
    if [[ -n "$__def" ]]; then
      read -r -p "$__msg [$__def]: " val
      [[ -z "$val" ]] && val="$__def"
    else
      read -r -p "$__msg: " val
    fi
  fi
  [[ -n "$val" ]] || die "Empty value for $__var"
  printf -v "$__var" "%s" "$val"
}

valid_domain(){
  local d="$1"
  [[ "$d" =~ ^[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]] || return 1
  [[ "$d" != *".."* ]] || return 1
  return 0
}

apt_install(){
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -y
  apt-get install -y "$@"
}

# ========= prompts =========
need_root

echo "=============================================="
echo "  MySite One-Line Installer (Fresh VPS Deploy)"
echo "  - Auto: Nginx + SSL + Gunicorn + Postgres"
echo "  - NOTE: This deploys EMPTY DB (no old posts)."
echo "=============================================="
echo

read_tty DOMAIN "New domain (e.g. example.com)"
valid_domain "$DOMAIN" || die "Invalid domain: $DOMAIN"
WWW_DOMAIN="www.${DOMAIN}"

read_tty SITE_NAME "Site name (brand/title)" 0 "Knowledge Sharing Hub"

read_tty ADMIN_USER "Admin username" 0 "admin"
read_tty ADMIN_EMAIL "Admin email" 0 "admin@${DOMAIN}"
read_tty ADMIN_PASS "Admin password" 1

read_tty DB_NAME "PostgreSQL DB name" 0 "mysite"
read_tty DB_USER "PostgreSQL DB user" 0 "mysiteuser"
read_tty DB_PASS "PostgreSQL DB password" 1

# repo settings (change defaults to your repo)
read_tty REPO_URL "GitHub repo URL (https://github.com/<you>/<repo>.git)"
read_tty REPO_BRANCH "Repo branch" 0 "main"

APP_DIR="/opt/mysite"
SERVICE_NAME="mysite"
GUNICORN_BIND="127.0.0.1:8001"

# ========= system deps =========
info "Installing packages..."
apt_install python3-venv python3-pip nginx postgresql postgresql-contrib certbot python3-certbot-nginx git ufw

# ========= firewall =========
info "Configuring UFW..."
ufw allow OpenSSH >/dev/null 2>&1 || true
ufw allow 80/tcp >/dev/null 2>&1 || true
ufw allow 443/tcp >/dev/null 2>&1 || true
ufw --force enable >/dev/null 2>&1 || true

# ========= code deploy =========
info "Deploying code to ${APP_DIR}..."
if [[ -d "${APP_DIR}/.git" ]]; then
  info "Repo exists. Pulling latest..."
  cd "$APP_DIR"
  git fetch --all
  git checkout "$REPO_BRANCH"
  git pull --ff-only origin "$REPO_BRANCH"
else
  rm -rf "$APP_DIR"
  git clone -b "$REPO_BRANCH" "$REPO_URL" "$APP_DIR"
fi

[[ -f "${APP_DIR}/manage.py" ]] || die "manage.py not found in ${APP_DIR}. Check repo root."

# ========= python venv =========
info "Setting up venv..."
python3 -m venv "${APP_DIR}/.venv"
source "${APP_DIR}/.venv/bin/activate"
pip install -U pip wheel
if [[ -f "${APP_DIR}/requirements.txt" ]]; then
  pip install -r "${APP_DIR}/requirements.txt"
else
  die "requirements.txt not found. Add it to repo."
fi

# ========= env file =========
info "Writing .env..."
SECRET_KEY="$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(48))
PY
)"


cat > "${APP_DIR}/.env" <<EOF
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=${SECRET_KEY}

DJANGO_ALLOWED_HOSTS=${DOMAIN},${WWW_DOMAIN}
DJANGO_CSRF_TRUSTED_ORIGINS=https://${DOMAIN},https://${WWW_DOMAIN}

DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASS=${DB_PASS}
DB_HOST=127.0.0.1
DB_PORT=5432

SITE_NAME=${SITE_NAME}
EOF
chmod 600 "${APP_DIR}/.env"

# ========= postgres (empty db) =========
info "Configuring PostgreSQL (empty DB)..."
sudo -u postgres psql <<SQL
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='${DB_USER}') THEN
    CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASS}';
  ELSE
    ALTER USER ${DB_USER} WITH PASSWORD '${DB_PASS}';
  END IF;
END
\$\$;

DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname='${DB_NAME}') THEN
    CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};
  END IF;
END
\$\$;

GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
SQL

# ========= django migrate + superuser =========
info "Running migrations..."
cd "$APP_DIR"

export DJANGO_SETTINGS_MODULE="config.settings"
export DJANGO_SUPERUSER_USERNAME="$ADMIN_USER"
export DJANGO_SUPERUSER_EMAIL="$ADMIN_EMAIL"
export DJANGO_SUPERUSER_PASSWORD="$ADMIN_PASS"

python manage.py migrate

# createsuperuser non-interactive (skip if exists)
python manage.py createsuperuser --noinput || true

info "Collecting static..."
python manage.py collectstatic --noinput

# ========= systemd gunicorn =========
info "Creating systemd service..."
cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<SERVICE
[Unit]
Description=${SERVICE_NAME} gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=${APP_DIR}
Environment="DJANGO_SETTINGS_MODULE=config.settings"
ExecStart=${APP_DIR}/.venv/bin/gunicorn config.wsgi:application --bind ${GUNICORN_BIND} --workers 2 --timeout 60
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable --now "${SERVICE_NAME}"

# ========= nginx =========
info "Configuring Nginx..."
rm -f /etc/nginx/sites-enabled/default || true

cat > "/etc/nginx/sites-available/${SERVICE_NAME}" <<NGINX
server {
    listen 80;
    server_name ${DOMAIN} ${WWW_DOMAIN};

    location /static/ {
        alias ${APP_DIR}/staticfiles/;
    }

    location /media/ {
        alias ${APP_DIR}/media/;
    }

    location / {
        proxy_pass http://${GUNICORN_BIND};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
NGINX

ln -sf "/etc/nginx/sites-available/${SERVICE_NAME}" "/etc/nginx/sites-enabled/${SERVICE_NAME}"
nginx -t
systemctl reload nginx

# ========= SSL =========
info "Issuing SSL (Let's Encrypt)..."
certbot --nginx -d "${DOMAIN}" -d "${WWW_DOMAIN}" --non-interactive --agree-tos -m "${ADMIN_EMAIL}" --redirect || die "Certbot failed. Check DNS A record & port 80 open."

# ========= done =========
echo
ok "Deployed successfully!"
echo "➡️  Site: https://${DOMAIN}"
echo "➡️  Admin panel: https://${DOMAIN}/panel/"
echo "➡️  Admin user: ${ADMIN_USER}"
echo
info "Service status:"
systemctl status "${SERVICE_NAME}" --no-pager || true
