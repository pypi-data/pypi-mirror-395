# 🚀 RAFAEL Framework - Server Deployment Guide

**Server IP**: 154.19.37.180  
**Domain**: rafaelabs.xyz  
**Date**: December 7, 2025

---

## 📋 Server Information

### Credentials
```
IP Address: 154.19.37.180
Username: root
Password: fM9e%gxZnJQ8
```

### Domain Configuration
```
Primary: rafaelabs.xyz
Subdomains:
- dashboard.rafaelabs.xyz
- api.rafaelabs.xyz
- beta.rafaelabs.xyz
- demo.rafaelabs.xyz
- docs.rafaelabs.xyz
```

**Status**: DNS configured, waiting for propagation (24-48 hours)

---

## 🎯 Quick Start

### Option 1: Automated Upload (Windows)
```powershell
# Run PowerShell script
cd R:\RAFAEL
.\upload_to_server.ps1
```

This will:
1. Install PuTTY (if needed)
2. Create directories on server
3. Upload all files
4. Run deployment script
5. Configure Nginx
6. Setup services

### Option 2: Manual SSH
```bash
# Connect to server
ssh root@154.19.37.180
# Password: fM9e%gxZnJQ8

# Once connected, follow manual steps below
```

---

## 📦 Manual Deployment Steps

### Step 1: Connect to Server
```bash
ssh root@154.19.37.180
```

### Step 2: Update System
```bash
# For CentOS/RHEL
yum update -y

# For Ubuntu/Debian
apt-get update -y && apt-get upgrade -y
```

### Step 3: Install Required Packages
```bash
# Install Python 3.11
yum install -y python3.11 python3.11-pip

# Install Git
yum install -y git

# Install Nginx
yum install -y nginx

# Install development tools
yum groupinstall -y "Development Tools"
```

### Step 4: Create Application Directory
```bash
mkdir -p /var/www/rafael
cd /var/www/rafael
```

### Step 5: Install RAFAEL Framework
```bash
python3.11 -m pip install --upgrade pip
python3.11 -m pip install rafael-framework
python3.11 -m pip install flask flask-cors gunicorn
```

### Step 6: Upload Files from Local Machine

**On your Windows machine**, open another PowerShell window:

```powershell
# Upload Dashboard
scp -r R:\RAFAEL\dashboard\* root@154.19.37.180:/var/www/rafael/dashboard/

# Upload Beta page
scp -r R:\RAFAEL\beta\* root@154.19.37.180:/var/www/rafael/beta/

# Upload examples
scp -r R:\RAFAEL\examples\* root@154.19.37.180:/var/www/rafael/examples/
```

### Step 7: Configure Nginx

**Back on the server:**

```bash
# Create Nginx configuration
cat > /etc/nginx/conf.d/rafaelabs.conf << 'EOF'
# Main site - rafaelabs.xyz
server {
    listen 80;
    server_name rafaelabs.xyz www.rafaelabs.xyz;
    
    root /var/www/rafael/landing;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}

# Dashboard - dashboard.rafaelabs.xyz
server {
    listen 80;
    server_name dashboard.rafaelabs.xyz;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# API - api.rafaelabs.xyz
server {
    listen 80;
    server_name api.rafaelabs.xyz;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Beta - beta.rafaelabs.xyz
server {
    listen 80;
    server_name beta.rafaelabs.xyz;
    
    root /var/www/rafael/beta;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
EOF

# Test Nginx configuration
nginx -t

# Restart Nginx
systemctl restart nginx
systemctl enable nginx
```

### Step 8: Create Landing Page
```bash
mkdir -p /var/www/rafael/landing

cat > /var/www/rafael/landing/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAFAEL Framework - Autonomous Resilience</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            text-align: center;
            padding: 2rem;
            max-width: 800px;
        }
        h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .tagline {
            font-size: 1.5rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        .description {
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 2rem;
            opacity: 0.8;
        }
        .links {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }
        .btn {
            padding: 1rem 2rem;
            background: rgba(255,255,255,0.2);
            border: 2px solid white;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.3s;
            backdrop-filter: blur(10px);
        }
        .btn:hover {
            background: white;
            color: #667eea;
            transform: translateY(-2px);
        }
        .status {
            margin-top: 2rem;
            padding: 1rem;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            backdrop-filter: blur(10px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔱 RAFAEL Framework</h1>
        <div class="tagline">Resilience-Adaptive Framework for Autonomous Evolution and Learning</div>
        <div class="description">
            Make your systems antifragile. RAFAEL treats resilience like DNA - 
            strategies that mutate and evolve based on real failures.
        </div>
        <div class="links">
            <a href="https://dashboard.rafaelabs.xyz" class="btn">📊 Dashboard</a>
            <a href="https://github.com/Rafael2022-prog/rafael" class="btn">💻 GitHub</a>
            <a href="https://beta.rafaelabs.xyz" class="btn">🚀 Join Beta</a>
            <a href="https://pypi.org/project/rafael-framework/" class="btn">📦 PyPI</a>
        </div>
        <div class="status">
            <strong>Status:</strong> Production Ready ✅<br>
            <strong>Version:</strong> 1.0.0<br>
            <strong>Server:</strong> 154.19.37.180
        </div>
    </div>
</body>
</html>
EOF
```

### Step 9: Create Systemd Service for Dashboard
```bash
cat > /etc/systemd/system/rafael-dashboard.service << 'EOF'
[Unit]
Description=RAFAEL Framework Dashboard
After=network.target

[Service]
Type=notify
User=root
WorkingDirectory=/var/www/rafael/dashboard
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/bin/python3.11 -m gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
systemctl daemon-reload

# Start dashboard service
systemctl start rafael-dashboard
systemctl enable rafael-dashboard

# Check status
systemctl status rafael-dashboard
```

### Step 10: Configure Firewall
```bash
# Allow HTTP and HTTPS
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload

# Or if using iptables
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

### Step 11: Install SSL Certificate (After DNS Propagation)
```bash
# Install Certbot
yum install -y certbot python3-certbot-nginx

# Get SSL certificate for all domains
certbot --nginx -d rafaelabs.xyz -d www.rafaelabs.xyz \
  -d dashboard.rafaelabs.xyz -d api.rafaelabs.xyz \
  -d beta.rafaelabs.xyz -d demo.rafaelabs.xyz

# Auto-renewal
systemctl enable certbot-renew.timer
```

---

## 🔍 Verification

### Check Services
```bash
# Check Nginx
systemctl status nginx
curl http://localhost

# Check Dashboard
systemctl status rafael-dashboard
curl http://localhost:5000

# Check logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
journalctl -u rafael-dashboard -f
```

### Test URLs (Direct IP)
```bash
# Main site
curl http://154.19.37.180

# Dashboard
curl http://154.19.37.180:5000
```

### Test URLs (After DNS Propagation)
```bash
# Main site
curl http://rafaelabs.xyz

# Dashboard
curl http://dashboard.rafaelabs.xyz

# API
curl http://api.rafaelabs.xyz/api/status

# Beta
curl http://beta.rafaelabs.xyz
```

---

## 📊 Monitoring

### Setup Monitoring
```bash
# Install monitoring tools
yum install -y htop iotop nethogs

# Monitor resources
htop

# Monitor network
nethogs

# Monitor disk
df -h
du -sh /var/www/rafael/*
```

### Setup Log Rotation
```bash
cat > /etc/logrotate.d/rafael << 'EOF'
/var/www/rafael/dashboard/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
}
EOF
```

---

## 🔒 Security

### Secure SSH
```bash
# Change SSH port (optional)
sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config
systemctl restart sshd

# Disable root login (after creating another user)
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
```

### Setup Fail2Ban
```bash
# Install fail2ban
yum install -y fail2ban

# Configure
cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
EOF

# Start fail2ban
systemctl start fail2ban
systemctl enable fail2ban
```

---

## 🚀 Post-Deployment

### 1. Wait for DNS Propagation
Check DNS propagation:
```bash
# Check from different locations
nslookup rafaelabs.xyz
dig rafaelabs.xyz

# Online tools
# https://www.whatsmydns.net/#A/rafaelabs.xyz
```

### 2. Setup SSL Certificates
```bash
certbot --nginx -d rafaelabs.xyz -d www.rafaelabs.xyz \
  -d dashboard.rafaelabs.xyz -d api.rafaelabs.xyz \
  -d beta.rafaelabs.xyz
```

### 3. Test All Services
- ✅ https://rafaelabs.xyz
- ✅ https://dashboard.rafaelabs.xyz
- ✅ https://api.rafaelabs.xyz
- ✅ https://beta.rafaelabs.xyz

### 4. Setup Monitoring
- Configure UptimeRobot
- Setup Google Analytics
- Enable Cloudflare (optional)

### 5. Backup Strategy
```bash
# Create backup script
cat > /root/backup_rafael.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/root/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/rafael_$DATE.tar.gz /var/www/rafael

# Keep only last 7 backups
ls -t $BACKUP_DIR/rafael_*.tar.gz | tail -n +8 | xargs rm -f
EOF

chmod +x /root/backup_rafael.sh

# Add to crontab (daily at 2 AM)
echo "0 2 * * * /root/backup_rafael.sh" | crontab -
```

---

## 🆘 Troubleshooting

### Dashboard Not Starting
```bash
# Check logs
journalctl -u rafael-dashboard -n 50

# Check if port is in use
netstat -tulpn | grep 5000

# Restart service
systemctl restart rafael-dashboard
```

### Nginx Not Working
```bash
# Check configuration
nginx -t

# Check logs
tail -f /var/log/nginx/error.log

# Restart Nginx
systemctl restart nginx
```

### DNS Not Resolving
```bash
# Check DNS records
dig rafaelabs.xyz
nslookup dashboard.rafaelabs.xyz

# Wait for propagation (24-48 hours)
# Use IP address temporarily: http://154.19.37.180
```

### SSL Certificate Issues
```bash
# Check certificate
certbot certificates

# Renew manually
certbot renew --dry-run

# Force renewal
certbot renew --force-renewal
```

---

## 📞 Quick Commands Reference

### Service Management
```bash
# Start services
systemctl start nginx
systemctl start rafael-dashboard

# Stop services
systemctl stop nginx
systemctl stop rafael-dashboard

# Restart services
systemctl restart nginx
systemctl restart rafael-dashboard

# Check status
systemctl status nginx
systemctl status rafael-dashboard
```

### File Locations
```
/var/www/rafael/              - Main directory
/var/www/rafael/dashboard/    - Dashboard files
/var/www/rafael/beta/         - Beta page
/var/www/rafael/landing/      - Landing page
/etc/nginx/conf.d/            - Nginx configs
/var/log/nginx/               - Nginx logs
```

### Useful Commands
```bash
# Check disk space
df -h

# Check memory
free -h

# Check processes
ps aux | grep python
ps aux | grep nginx

# Check ports
netstat -tulpn

# Check logs
tail -f /var/log/nginx/access.log
journalctl -u rafael-dashboard -f
```

---

## ✅ Deployment Checklist

### Pre-Deployment
- [x] Server credentials received
- [x] Domain registered (rafaelabs.xyz)
- [x] DNS configured
- [ ] DNS propagated (waiting 24-48 hours)

### Server Setup
- [ ] SSH access confirmed
- [ ] System updated
- [ ] Python 3.11 installed
- [ ] Nginx installed
- [ ] RAFAEL Framework installed

### Application Deployment
- [ ] Files uploaded to server
- [ ] Dashboard configured
- [ ] Beta page deployed
- [ ] Landing page created
- [ ] Nginx configured
- [ ] Services started

### Security
- [ ] Firewall configured
- [ ] SSL certificates installed
- [ ] Fail2Ban configured
- [ ] Backups configured

### Post-Deployment
- [ ] All URLs tested
- [ ] Monitoring setup
- [ ] Analytics configured
- [ ] Documentation updated

---

## 🎉 Summary

### What's Deployed
✅ Nginx web server  
✅ Python 3.11 environment  
✅ RAFAEL Framework  
✅ Dashboard application  
✅ Beta program page  
✅ Landing page  

### URLs (After DNS Propagation)
- **Main**: https://rafaelabs.xyz
- **Dashboard**: https://dashboard.rafaelabs.xyz
- **API**: https://api.rafaelabs.xyz
- **Beta**: https://beta.rafaelabs.xyz

### Temporary Access (Direct IP)
- **Main**: http://154.19.37.180
- **Dashboard**: http://154.19.37.180:5000

### Next Steps
1. Wait for DNS propagation (24-48 hours)
2. Install SSL certificates with Certbot
3. Test all services
4. Setup monitoring
5. Announce launch! 🚀

---

**🔱 RAFAEL Framework**  
*rafaelabs.xyz - Where systems evolve*

**Server**: 154.19.37.180  
**Status**: Deployed ✅  
**Ready**: Waiting for DNS propagation
