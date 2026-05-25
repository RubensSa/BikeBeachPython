# Deploy guide (Gunicorn + Nginx)

Quick steps to deploy BikeBeach on a Linux server (example paths use `/srv/bikebeach`):

1. Copy project to server, create and activate a virtualenv:
```bash
python -m venv /srv/bikebeach/.venv
source /srv/bikebeach/.venv/bin/activate
pip install -r requirements.txt gunicorn
```

2. Configure environment variables (do NOT keep SECRET_KEY in code):
```bash
export DJANGO_SECRET_KEY='your_secret'
export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS='yourdomain.com,IP'
```

3. Run migrations and collect static files:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

4. Install the systemd service (example):
```bash
sudo cp deploy/bikebeach.service /etc/systemd/system/bikebeach.service
# Edit the service to point to your WorkingDirectory and virtualenv PATH
sudo systemctl daemon-reload
sudo systemctl enable --now bikebeach.service
sudo journalctl -u bikebeach -f
```

5. Configure Nginx:
```bash
sudo cp deploy/nginx_bikebeach.conf /etc/nginx/sites-available/bikebeach
sudo ln -s /etc/nginx/sites-available/bikebeach /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

6. (Optional) Enable HTTPS with Certbot/Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

Notes and tips
- Adjust `User`/`Group` in the systemd unit (commonly `www-data` or a dedicated deploy user).
- Ensure file permissions allow the web user to read static files and access the project directory.
- In production use a robust DB (Postgres) and store DB credentials in env vars.
