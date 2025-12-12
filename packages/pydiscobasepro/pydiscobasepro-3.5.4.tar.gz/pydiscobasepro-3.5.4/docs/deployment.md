---
layout: default
title: Deployment
nav_order: 5
---

# Deployment Guide

## Local Development

For development and testing:

```bash
pip install -e .
python bot.py
```

Use hot-reloading for rapid development without restarts.

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash botuser
USER botuser

# Expose dashboard port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

CMD ["python", "bot.py"]
```

### Build and Run

```bash
docker build -t pydiscobasepro .
docker run -d --name mybot \
  -e BOT_TOKEN=your_token_here \
  -e MONGODB_URI=mongodb://host.docker.internal:27017 \
  -p 8080:8080 \
  pydiscobasepro
```

## PM2 Process Manager

### Installation

```bash
npm install -g pm2
pm2 startup
sudo env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u $USER --hp $HOME
```

### PM2 Configuration

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'PyDiscoBasePro',
    script: 'bot.py',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
};
```

### Start with PM2

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 monit
```

## Systemd Service

### Service File

```ini
[Unit]
Description=PyDiscoBasePro Discord Bot
After=network.target mongodb.service

[Service]
Type=simple
User=botuser
Group=botuser
WorkingDirectory=/opt/pydiscobasepro
Environment="PATH=/opt/pydiscobasepro/venv/bin"
ExecStart=/opt/pydiscobasepro/venv/bin/python bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Installation Steps

```bash
sudo cp pydiscobasepro.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable pydiscobasepro
sudo systemctl start pydiscobasepro
sudo systemctl status pydiscobasepro
```

## Cloud Deployment

### Heroku

```txt
# requirements.txt (add gunicorn)
gunicorn==20.1.0

# Procfile
web: python bot.py
worker: python bot.py

# Deploy
git push heroku main
```

### DigitalOcean App Platform

Use the Dockerfile above and deploy directly from GitHub.

### AWS EC2

```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip mongodb

# Clone and setup
git clone https://github.com/code-xon/pydiscobasepro.git
cd pydiscobasepro
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure systemd service (see above)
sudo systemctl enable pydiscobasepro
sudo systemctl start pydiscobasepro
```

## Database Setup

### MongoDB Local

```bash
# Ubuntu/Debian
sudo apt install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb

# macOS with Homebrew
brew install mongodb-community
brew services start mongodb-community

# Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### MongoDB Atlas (Cloud)

1. Create account at [MongoDB Atlas](https://cloud.mongodb.com)
2. Create a cluster
3. Get connection string
4. Update config.json with the URI

## Monitoring & Maintenance

### Log Rotation

```txt
# logrotate configuration
/var/log/pydiscobasepro/*.log {
    daily
    missingok
    rotate 7
    compress
    notifempty
    create 0644 botuser botuser
    postrotate
        systemctl reload pydiscobasepro
    endscript
}
```

### Health Checks

```bash
curl http://localhost:8080/health
```

### Backup Strategy

```bash
# MongoDB backup
mongodump --db pydiscobasepro --out /backup/$(date +%Y%m%d)

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mongodump --db pydiscobasepro --out /backup/backup_$DATE
find /backup -name "backup_*" -mtime +7 -delete
```

## Security Best Practices

- Use environment variables for sensitive data
- Run bot as non-root user
- Enable firewall (ufw/iptables)
- Regular security updates
- Monitor logs for suspicious activity
- Use HTTPS for dashboard in production