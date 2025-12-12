---
layout: default
title: Deployment
nav_order: 5
---

<div class="page-header">
  <h1><i class="fas fa-server"></i> Deployment Guide</h1>
  <p class="page-subtitle">Deploy your PyDiscoBasePro bot to production with confidence using Docker, cloud platforms, and monitoring</p>
</div>

## 🏠 Local Development

<div class="dev-setup">
  <div class="dev-step">
    <h3>1. Development Installation</h3>
    <div class="code-tabs">
      <div class="tab-buttons">
        <button class="tab-btn active" data-tab="pip-dev">pip (Development)</button>
        <button class="tab-btn" data-tab="docker-dev">Docker (Development)</button>
      </div>

      <div class="tab-content">
        <div class="tab-pane active" id="pip-dev">
```bash
# Clone the repository
git clone https://github.com/code-xon/pydiscobasepro.git
cd pydiscobasepro

# Install in development mode
pip install -e .

# Create a development project
pydiscobasepro project create dev-bot --template basic

# Navigate to project
cd dev-bot

# Install project dependencies
pip install -r requirements.txt

# Start with hot-reload
python bot.py
```
        </div>

        <div class="tab-pane" id="docker-dev">
```bash
# Use the development Docker image
docker run -it --rm \
  -v $(pwd):/app \
  -p 8080:8080 \
  code-xon/pydiscobasepro:latest \
  bash

# Inside container
cd /app
pip install -e .
pydiscobasepro project create dev-bot
cd dev-bot && python bot.py
```
        </div>
      </div>
    </div>
  </div>

  <div class="dev-features">
    <h3>Development Features</h3>
    <div class="feature-grid">
      <div class="feature-item">
        <i class="fas fa-sync-alt"></i>
        <h4>Hot Reload</h4>
        <p>Automatically reload commands and events on file changes</p>
      </div>

      <div class="feature-item">
        <i class="fas fa-bug"></i>
        <h4>Debug Mode</h4>
        <p>Detailed logging and error reporting for development</p>
      </div>

      <div class="feature-item">
        <i class="fas fa-flask"></i>
        <h4>Test Environment</h4>
        <p>Isolated testing environment with mock services</p>
      </div>

      <div class="feature-item">
        <i class="fas fa-terminal"></i>
        <h4>CLI Tools</h4>
        <p>Comprehensive command-line tools for development</p>
      </div>
    </div>
  </div>
</div>

## 🐳 Docker Deployment

### Quick Docker Setup

<div class="docker-setup">
  <div class="docker-step">
    <h3>1. Create Dockerfile</h3>
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash botuser

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership
RUN chown -R botuser:botuser /app
USER botuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import asyncio; from pydiscobasepro import PyDiscoBasePro; print('OK')" || exit 1

# Expose dashboard port
EXPOSE 8080

# Run the bot
CMD ["python", "bot.py"]
```
  </div>

  <div class="docker-step">
    <h3>2. Create docker-compose.yml</h3>
```yaml
version: '3.8'

services:
  discord-bot:
    build: .
    container_name: pydiscobasepro-bot
    restart: unless-stopped
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN}
      - MONGODB_URI=mongodb://mongodb:27017
      - REDIS_URL=redis://redis:6379
    ports:
      - "8080:8080"
    depends_on:
      - mongodb
      - redis
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    networks:
      - bot-network

  mongodb:
    image: mongo:7.0
    container_name: pydiscobasepro-mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
      MONGO_INITDB_DATABASE: discord_bot
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
      - ./docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d:ro
    networks:
      - bot-network

  redis:
    image: redis:7.2-alpine
    container_name: pydiscobasepro-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - bot-network

  # Optional: Monitoring stack
  prometheus:
    image: prom/prometheus:latest
    container_name: pydiscobasepro-prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - bot-network
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  grafana:
    image: grafana/grafana:latest
    container_name: pydiscobasepro-grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - bot-network

networks:
  bot-network:
    driver: bridge

volumes:
  mongodb_data:
  redis_data:
  prometheus_data:
  grafana_data:
```
  </div>

  <div class="docker-step">
    <h3>3. Environment Variables</h3>
```bash
# Create .env file
cat > .env << EOF
DISCORD_TOKEN=your_bot_token_here
MONGODB_URI=mongodb://mongodb:27017
REDIS_URL=redis://redis:6379
LOG_LEVEL=INFO
DASHBOARD_SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=32-character-encryption-key-here
EOF
```
  </div>

  <div class="docker-step">
    <h3>4. Deploy with Docker Compose</h3>
```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f discord-bot

# Check health
docker-compose ps

# Scale the bot (if needed)
docker-compose up -d --scale discord-bot=2

# Update deployment
docker-compose pull && docker-compose up -d

# Stop everything
docker-compose down
```
  </div>
</div>

## ☁️ Cloud Deployment

### AWS Deployment

<div class="cloud-deployment">
  <div class="cloud-provider">
    <h3><i class="fab fa-aws"></i> Amazon Web Services</h3>

    <div class="deployment-steps">
      <div class="step">
        <h4>1. EC2 Instance Setup</h4>
```bash
# Launch EC2 instance (t3.micro for small bots, t3.medium+ for larger)
# AMI: Amazon Linux 2 or Ubuntu 22.04
# Security Group: Allow SSH (22), HTTP (80), HTTPS (443), Custom TCP (8080)

# Connect to instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Update system
sudo yum update -y  # Amazon Linux
# or
sudo apt update && sudo apt upgrade -y  # Ubuntu

# Install Docker
sudo yum install -y docker  # Amazon Linux
# or
sudo apt install -y docker.io  # Ubuntu

sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user
```
      </div>

      <div class="step">
        <h4>2. Deploy with Docker</h4>
```bash
# Clone your bot repository
git clone https://github.com/yourusername/your-bot-repo.git
cd your-bot-repo

# Create environment file
cat > .env << EOF
DISCORD_TOKEN=${DISCORD_TOKEN}
MONGODB_URI=${MONGODB_URI}
AWS_REGION=us-east-1
EOF

# Deploy
docker-compose up --build -d

# Setup SSL with Let's Encrypt (optional)
sudo amazon-linux-extras install nginx1 -y
sudo systemctl start nginx
sudo systemctl enable nginx

# Configure nginx for SSL termination
```
      </div>

      <div class="step">
        <h4>3. Monitoring & Scaling</h4>
```bash
# Install CloudWatch agent
sudo yum install -y amazon-cloudwatch-agent
sudo systemctl enable amazon-cloudwatch-agent
sudo systemctl start amazon-cloudwatch-agent

# Setup auto-scaling (if needed)
# Use AWS ECS or EKS for container orchestration
# Configure load balancer for high availability
```
      </div>
    </div>
  </div>

  <div class="cloud-provider">
    <h3><i class="fab fa-google"></i> Google Cloud Platform</h3>

    <div class="deployment-steps">
      <div class="step">
        <h4>1. Cloud Run Setup</h4>
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/discord-bot

# Deploy to Cloud Run
gcloud run deploy discord-bot \
  --image gcr.io/PROJECT-ID/discord-bot \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars DISCORD_TOKEN=your_token \
  --set-env-vars MONGODB_URI=your_mongodb_uri \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 900
```
      </div>

      <div class="step">
        <h4>2. Firestore Database</h4>
```bash
# Use Firestore instead of MongoDB
export GOOGLE_CLOUD_PROJECT=your-project-id

# Bot will automatically use Firestore when configured
```
      </div>
    </div>
  </div>

  <div class="cloud-provider">
    <h3><i class="fab fa-microsoft"></i> Microsoft Azure</h3>

    <div class="deployment-steps">
      <div class="step">
        <h4>1. Azure Container Instances</h4>
```bash
# Build and push to Azure Container Registry
az acr build --registry yourregistry --image discord-bot .

# Deploy to ACI
az container create \
  --resource-group yourResourceGroup \
  --name discord-bot \
  --image yourregistry.azurecr.io/discord-bot:latest \
  --cpu 1 \
  --memory 1 \
  --registry-login-server yourregistry.azurecr.io \
  --registry-username yourregistry \
  --registry-password yourpassword \
  --environment-variables DISCORD_TOKEN=your_token \
  --ports 8080 \
  --dns-name-label discord-bot-$(date +%s)
```
      </div>

      <div class="step">
        <h4>2. Azure Database for MongoDB</h4>
```bash
# Create Azure Cosmos DB with MongoDB API
az cosmosdb create \
  --name your-cosmos-db \
  --resource-group yourResourceGroup \
  --kind MongoDB \
  --server-version 4.0

# Get connection string
az cosmosdb keys list \
  --name your-cosmos-db \
  --resource-group yourResourceGroup \
  --type connection-strings
```
      </div>
    </div>
  </div>
</div>

## 🚀 Advanced Deployment Strategies

### Blue-Green Deployment

```bash
# Create blue environment
docker tag mybot:latest mybot:blue
docker-compose -f docker-compose.blue.yml up -d

# Test blue environment
curl http://blue-environment/health

# Switch traffic to blue
docker-compose -f docker-compose.green.yml down
docker tag mybot:blue mybot:live

# Cleanup old green environment
docker-compose -f docker-compose.green.yml down
```

### Canary Deployment

```yaml
# docker-compose.canary.yml
version: '3.8'
services:
  bot-canary:
    image: mybot:latest
    environment:
      - CANARY_MODE=true
      - TRAFFIC_PERCENTAGE=10
    deploy:
      replicas: 1
    labels:
      - "canary=true"
```

### Rolling Updates

```bash
# Zero-downtime updates
docker-compose up -d --scale discord-bot=2
docker-compose up -d --scale discord-bot=1

# Or use rolling update strategy
docker service update \
  --image mybot:new-version \
  --update-parallelism 1 \
  --update-delay 30s \
  mybot_service
```

## 📊 Monitoring & Observability

### Application Monitoring

<div class="monitoring-setup">
  <div class="monitoring-tool">
    <h4>Prometheus Metrics</h4>
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'discord-bot'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: '/metrics'
```
  </div>

  <div class="monitoring-tool">
    <h4>Grafana Dashboards</h4>
```json
{
  "dashboard": {
    "title": "Discord Bot Metrics",
    "panels": [
      {
        "title": "Command Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(discord_bot_commands_total[5m])",
            "legendFormat": "{{command}}"
          }
        ]
      }
    ]
  }
}
```
  </div>
</div>

### Health Checks & Alerts

```json
{
  "health_checks": {
    "endpoints": [
      {
        "name": "bot_health",
        "url": "http://localhost:8080/health",
        "interval": 30,
        "timeout": 10
      },
      {
        "name": "discord_api",
        "url": "https://discord.com/api/v10/users/@me",
        "headers": {"Authorization": "Bot ${DISCORD_TOKEN}"},
        "interval": 60
      }
    ],
    "alerts": {
      "slack": {
        "webhook_url": "https://hooks.slack.com/...",
        "channel": "#alerts"
      },
      "discord": {
        "webhook_url": "https://discord.com/api/webhooks/...",
        "username": "Bot Monitor"
      }
    }
  }
}
```

## 🔧 Process Management

### systemd Service

```ini
# /etc/systemd/system/discord-bot.service
[Unit]
Description=PyDiscoBasePro Discord Bot
After=network.target mongodb.service redis.service
Requires=mongodb.service redis.service

[Service]
Type=simple
User=botuser
Group=botuser
WorkingDirectory=/opt/discord-bot
EnvironmentFile=/opt/discord-bot/.env
ExecStart=/opt/discord-bot/venv/bin/python bot.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5

# Security settings
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ReadWritePaths=/opt/discord-bot/logs /opt/discord-bot/data

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable discord-bot
sudo systemctl start discord-bot

# View logs
sudo journalctl -u discord-bot -f

# Restart service
sudo systemctl restart discord-bot
```

### PM2 Process Manager

```bash
# Install PM2 globally
npm install -g pm2

# Create ecosystem file
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'discord-bot',
    script: 'bot.py',
    interpreter: 'python3',
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
EOF

# Start with PM2
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save

# Setup PM2 to start on boot
pm2 startup
sudo env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u $USER --hp $HOME

# Monitor processes
pm2 monit
pm2 logs discord-bot
```

## 🔒 Security Best Practices

### Production Security

<div class="security-checklist">
  <h3>Security Checklist</h3>

  <div class="security-item">
    <input type="checkbox" checked>
    <label>Use environment variables for secrets</label>
  </div>

  <div class="security-item">
    <input type="checkbox" checked>
    <label>Enable SSL/TLS for dashboard</label>
  </div>

  <div class="security-item">
    <input type="checkbox" checked>
    <label>Configure firewall rules</label>
  </div>

  <div class="security-item">
    <input type="checkbox" checked>
    <label>Use non-root user for bot process</label>
  </div>

  <div class="security-item">
    <input type="checkbox" checked>
    <label>Enable rate limiting</label>
  </div>

  <div class="security-item">
    <input type="checkbox" checked>
    <label>Regular security updates</label>
  </div>

  <div class="security-item">
    <input type="checkbox" checked>
    <label>Monitor for vulnerabilities</label>
  </div>

  <div class="security-item">
    <input type="checkbox" checked>
    <label>Backup critical data</label>
  </div>
</div>

### SSL/TLS Configuration

```nginx
# nginx.conf for SSL termination
server {
    listen 80;
    server_name your-bot-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-bot-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-bot-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-bot-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🚨 Backup & Recovery

### Automated Backups

```bash
#!/bin/bash
# backup.sh - Automated backup script

BACKUP_DIR="/opt/discord-bot/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
docker exec mongodb mongodump --db discord_bot --out /backup
docker cp mongodb:/backup $BACKUP_DIR/mongodb_$DATE

# Configuration backup
tar -czf $BACKUP_DIR/config_$DATE.tar.gz /opt/discord-bot/config/

# Logs backup (last 7 days)
find /opt/discord-bot/logs -name "*.log" -mtime -7 -exec tar -czf $BACKUP_DIR/logs_$DATE.tar.gz {} +

# Clean old backups (keep last 30)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

### Disaster Recovery

```bash
#!/bin/bash
# restore.sh - Disaster recovery script

BACKUP_DATE=$1
BACKUP_DIR="/opt/discord-bot/backups"

if [ -z "$BACKUP_DATE" ]; then
    echo "Usage: $0 <backup_date>"
    echo "Available backups:"
    ls -la $BACKUP_DIR | grep tar.gz
    exit 1
fi

# Stop services
docker-compose down

# Restore database
docker cp $BACKUP_DIR/mongodb_$BACKUP_DATE mongodb:/
docker exec mongodb mongorestore --db discord_bot /backup/discord_bot

# Restore configuration
tar -xzf $BACKUP_DIR/config_$BACKUP_DATE.tar.gz -C /

# Start services
docker-compose up -d

echo "Restoration completed from: $BACKUP_DATE"
```

## 📈 Performance Optimization

### Production Optimizations

```json
{
  "production_optimizations": {
    "caching": {
      "enabled": true,
      "redis_cluster": true,
      "cache_warming": true
    },
    "database": {
      "connection_pooling": true,
      "query_optimization": true,
      "read_replicas": true
    },
    "concurrency": {
      "worker_processes": 4,
      "async_tasks": true,
      "connection_limits": 1000
    },
    "monitoring": {
      "performance_metrics": true,
      "memory_profiling": true,
      "cpu_profiling": true
    }
  }
}
```

### Scaling Strategies

<div class="scaling-strategies">
  <div class="strategy">
    <h4>Horizontal Scaling</h4>
    <ul>
      <li>Multiple bot instances behind load balancer</li>
      <li>Shared Redis cache for session management</li>
      <li>Database read replicas for query distribution</li>
      <li>Message queue for inter-instance communication</li>
    </ul>
  </div>

  <div class="strategy">
    <h4>Vertical Scaling</h4>
    <ul>
      <li>Increase CPU cores and memory</li>
      <li>Optimize database queries and indexes</li>
      <li>Implement efficient caching strategies</li>
      <li>Use faster storage solutions</li>
    </ul>
  </div>

  <div class="strategy">
    <h4>Database Scaling</h4>
    <ul>
      <li>Implement database sharding</li>
      <li>Use connection pooling</li>
      <li>Optimize query performance</li>
      <li>Implement database caching layers</li>
    </ul>
  </div>
</div>

## 🆘 Troubleshooting Deployment

<div class="troubleshooting">
  <details>
    <summary><strong>Bot not starting after deployment?</strong></summary>
    <ul>
      <li>Check environment variables are set correctly</li>
      <li>Verify database connectivity</li>
      <li>Check file permissions on logs and data directories</li>
      <li>Review application logs for error messages</li>
      <li>Ensure all required ports are open</li>
    </ul>
  </details>

  <details>
    <summary><strong>High memory usage in production?</strong></summary>
    <ul>
      <li>Enable garbage collection tuning</li>
      <li>Implement memory profiling</li>
      <li>Check for memory leaks in plugins</li>
      <li>Configure appropriate cache sizes</li>
      <li>Monitor memory usage with tools like Valgrind</li>
    </ul>
  </details>

  <details>
    <summary><strong>Database connection issues?</strong></summary>
    <ul>
      <li>Verify connection string format</li>
      <li>Check network connectivity to database</li>
      <li>Ensure database credentials are correct</li>
      <li>Configure appropriate connection timeouts</li>
      <li>Implement connection pooling</li>
    </ul>
  </details>
</div>

## 📞 Support & Resources

<div class="support-resources">
  <div class="resource">
    <i class="fab fa-github"></i>
    <div>
      <h4>GitHub Repository</h4>
      <p>Report issues and contribute to the project</p>
      <a href="https://github.com/code-xon/pydiscobasepro">View Repository</a>
    </div>
  </div>

  <div class="resource">
    <i class="fab fa-discord"></i>
    <div>
      <h4>Community Discord</h4>
      <p>Get help from the community and developers</p>
      <a href="https://discord.gg/pydiscobasepro">Join Discord</a>
    </div>
  </div>

  <div class="resource">
    <i class="fas fa-book"></i>
    <div>
      <h4>Documentation</h4>
      <p>Comprehensive guides and API reference</p>
      <a href="api.html">Browse Docs</a>
    </div>
  </div>

  <div class="resource">
    <i class="fas fa-life-ring"></i>
    <div>
      <h4>Professional Support</h4>
      <p>Enterprise support and consulting services</p>
      <a href="mailto:support@pydiscobasepro.com">Contact Support</a>
    </div>
  </div>
</div>
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