#!/bin/bash

# RAFAEL Framework - Server Deployment Script
# Server: 154.19.37.180
# Domain: rafaelabs.xyz

echo "=========================================="
echo "RAFAEL Framework - Server Deployment"
echo "=========================================="
echo ""

# Update system
echo "1. Updating system packages..."
sudo yum update -y || sudo apt-get update -y

# Install Python 3.11+
echo "2. Installing Python 3.11..."
sudo yum install -y python3.11 python3.11-pip || sudo apt-get install -y python3.11 python3.11-pip

# Install Git
echo "3. Installing Git..."
sudo yum install -y git || sudo apt-get install -y git

# Install Nginx
echo "4. Installing Nginx..."
sudo yum install -y nginx || sudo apt-get install -y nginx

# Create application directory
echo "5. Creating application directory..."
sudo mkdir -p /var/www/rafael
cd /var/www/rafael

# Clone or copy RAFAEL repository
echo "6. Setting up RAFAEL Framework..."
# If using Git:
# git clone https://github.com/Rafael2022-prog/rafael.git .

# Install Python dependencies
echo "7. Installing Python dependencies..."
python3.11 -m pip install --upgrade pip
python3.11 -m pip install rafael-framework
python3.11 -m pip install flask flask-cors gunicorn

# Setup Dashboard
echo "8. Setting up Dashboard..."
mkdir -p /var/www/rafael/dashboard

# Create systemd service for Dashboard
echo "9. Creating systemd service..."
sudo tee /etc/systemd/system/rafael-dashboard.service > /dev/null <<EOF
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

# Configure Nginx for main site
echo "10. Configuring Nginx for rafaelabs.xyz..."
sudo tee /etc/nginx/conf.d/rafaelabs.conf > /dev/null <<EOF
# Main site - rafaelabs.xyz
server {
    listen 80;
    server_name rafaelabs.xyz www.rafaelabs.xyz;
    
    root /var/www/rafael/landing;
    index index.html;
    
    location / {
        try_files \$uri \$uri/ =404;
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
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}

# API - api.rafaelabs.xyz
server {
    listen 80;
    server_name api.rafaelabs.xyz;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}

# Beta - beta.rafaelabs.xyz
server {
    listen 80;
    server_name beta.rafaelabs.xyz;
    
    root /var/www/rafael/beta;
    index index.html;
    
    location / {
        try_files \$uri \$uri/ =404;
    }
}

# Demo - demo.rafaelabs.xyz
server {
    listen 80;
    server_name demo.rafaelabs.xyz;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Create landing page directory
echo "11. Creating landing page..."
sudo mkdir -p /var/www/rafael/landing
sudo tee /var/www/rafael/landing/index.html > /dev/null <<EOF
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
            <strong>Domain:</strong> rafaelabs.xyz
        </div>
    </div>
</body>
</html>
EOF

# Test Nginx configuration
echo "12. Testing Nginx configuration..."
sudo nginx -t

# Restart services
echo "13. Starting services..."
sudo systemctl restart nginx
sudo systemctl enable nginx

# Install Certbot for SSL (Let's Encrypt)
echo "14. Installing Certbot for SSL..."
sudo yum install -y certbot python3-certbot-nginx || sudo apt-get install -y certbot python3-certbot-nginx

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Wait for DNS propagation (24-48 hours)"
echo "2. Upload dashboard files to /var/www/rafael/dashboard"
echo "3. Upload beta page to /var/www/rafael/beta"
echo "4. Run: sudo certbot --nginx -d rafaelabs.xyz -d www.rafaelabs.xyz"
echo "5. Start dashboard: sudo systemctl start rafael-dashboard"
echo ""
echo "URLs (after DNS propagation):"
echo "- https://rafaelabs.xyz"
echo "- https://dashboard.rafaelabs.xyz"
echo "- https://api.rafaelabs.xyz"
echo "- https://beta.rafaelabs.xyz"
echo ""
echo "Server IP: 154.19.37.180"
echo "=========================================="
