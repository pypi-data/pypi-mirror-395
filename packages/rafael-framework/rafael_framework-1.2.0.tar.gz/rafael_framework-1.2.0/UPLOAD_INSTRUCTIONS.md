# 📤 Upload Files to Server - Step by Step

**Server**: 154.19.37.180  
**Username**: root  
**Password**: fM9e%gxZnJQ8

---

## 🎯 Method 1: Using WinSCP (Recommended - GUI)

### Step 1: Download WinSCP
1. Download from: https://winscp.net/eng/download.php
2. Install WinSCP

### Step 2: Connect to Server
1. Open WinSCP
2. Enter connection details:
   - **File protocol**: SFTP
   - **Host name**: 154.19.37.180
   - **Port number**: 22
   - **User name**: root
   - **Password**: fM9e%gxZnJQ8
3. Click "Login"
4. Accept the host key when prompted

### Step 3: Upload Files
1. Navigate to `/var/www/` on the server (right panel)
2. Create folder `rafael` if it doesn't exist
3. Navigate to `R:\RAFAEL` on your computer (left panel)
4. Drag and drop these folders to `/var/www/rafael/`:
   - `dashboard/`
   - `beta/`
   - `examples/`
   - `docs/`

### Step 4: Upload Deployment Script
1. Navigate to `/root/` on the server
2. Upload `deploy_to_server.sh` from `R:\RAFAEL\`

---

## 🎯 Method 2: Using PuTTY + PSCP (Command Line)

### Step 1: Install PuTTY
```powershell
# Install via winget
winget install -e --id PuTTY.PuTTY

# Or download from: https://www.putty.org/
```

### Step 2: Connect via PuTTY First (Accept Host Key)
1. Open PuTTY
2. Enter:
   - **Host Name**: 154.19.37.180
   - **Port**: 22
3. Click "Open"
4. Click "Accept" when asked about host key
5. Login:
   - **Username**: root
   - **Password**: fM9e%gxZnJQ8
6. Keep this window open

### Step 3: Upload Files via PSCP
Open **NEW** PowerShell window:

```powershell
cd R:\RAFAEL

# Upload deployment script
pscp -pw "fM9e%gxZnJQ8" deploy_to_server.sh root@154.19.37.180:/root/

# Upload dashboard
pscp -pw "fM9e%gxZnJQ8" -r dashboard root@154.19.37.180:/var/www/rafael/

# Upload beta page
pscp -pw "fM9e%gxZnJQ8" -r beta root@154.19.37.180:/var/www/rafael/

# Upload examples
pscp -pw "fM9e%gxZnJQ8" -r examples root@154.19.37.180:/var/www/rafael/
```

---

## 🎯 Method 3: Manual SSH Commands

### Step 1: Connect to Server
```powershell
ssh root@154.19.37.180
# Password: fM9e%gxZnJQ8
```

### Step 2: Create Directories
```bash
mkdir -p /var/www/rafael/dashboard
mkdir -p /var/www/rafael/beta
mkdir -p /var/www/rafael/landing
mkdir -p /var/www/rafael/examples
```

### Step 3: Install Required Software
```bash
# Update system
yum update -y

# Install Python 3.11
yum install -y python3.11 python3.11-pip

# Install Nginx
yum install -y nginx

# Install Git
yum install -y git

# Install RAFAEL Framework
python3.11 -m pip install --upgrade pip
python3.11 -m pip install rafael-framework flask flask-cors gunicorn
```

### Step 4: Create Landing Page
```bash
cat > /var/www/rafael/landing/index.html << 'HTMLEOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAFAEL Framework</title>
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
            padding: 2rem;
        }
        .container {
            text-align: center;
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
        .links {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 2rem;
        }
        .btn {
            padding: 1rem 2rem;
            background: rgba(255,255,255,0.2);
            border: 2px solid white;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            transition: all 0.3s;
            backdrop-filter: blur(10px);
        }
        .btn:hover {
            background: white;
            color: #667eea;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔱 RAFAEL Framework</h1>
        <div class="tagline">Resilience-Adaptive Framework for Autonomous Evolution and Learning</div>
        <div class="links">
            <a href="https://dashboard.rafaelabs.xyz" class="btn">📊 Dashboard</a>
            <a href="https://github.com/Rafael2022-prog/rafael" class="btn">💻 GitHub</a>
            <a href="https://beta.rafaelabs.xyz" class="btn">🚀 Beta</a>
        </div>
    </div>
</body>
</html>
HTMLEOF
```

### Step 5: Configure Nginx
```bash
cat > /etc/nginx/conf.d/rafaelabs.conf << 'NGINXEOF'
server {
    listen 80 default_server;
    server_name rafaelabs.xyz www.rafaelabs.xyz 154.19.37.180;
    
    root /var/www/rafael/landing;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}

server {
    listen 80;
    server_name dashboard.rafaelabs.xyz;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;
    server_name beta.rafaelabs.xyz;
    
    root /var/www/rafael/beta;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
NGINXEOF

# Test and restart Nginx
nginx -t
systemctl restart nginx
systemctl enable nginx
```

### Step 6: Configure Firewall
```bash
# Allow HTTP and HTTPS
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload
```

### Step 7: Test
```bash
# Test landing page
curl http://localhost

# Check if Nginx is running
systemctl status nginx
```

---

## ✅ Verification

### Check from Your Browser

**Direct IP Access (Works immediately)**:
- http://154.19.37.180

**Domain Access (After DNS propagation)**:
- http://rafaelabs.xyz
- http://dashboard.rafaelabs.xyz
- http://beta.rafaelabs.xyz

### Check DNS Propagation
Visit: https://www.whatsmydns.net/
- Enter: rafaelabs.xyz
- Check if it resolves to: 154.19.37.180

---

## 🚀 After Files Are Uploaded

### 1. Run Deployment Script
```bash
ssh root@154.19.37.180
cd /root
chmod +x deploy_to_server.sh
./deploy_to_server.sh
```

### 2. Start Dashboard
```bash
cd /var/www/rafael/dashboard
python3.11 -m gunicorn --workers 4 --bind 0.0.0.0:5000 app:app --daemon
```

### 3. Setup SSL (After DNS Propagation)
```bash
# Install Certbot
yum install -y certbot python3-certbot-nginx

# Get SSL certificate
certbot --nginx -d rafaelabs.xyz -d www.rafaelabs.xyz \
  -d dashboard.rafaelabs.xyz -d beta.rafaelabs.xyz

# Follow prompts:
# - Enter email address
# - Agree to terms
# - Choose redirect HTTP to HTTPS
```

---

## 📊 Quick Status Check

### On Server
```bash
# Check Nginx
systemctl status nginx

# Check if port 80 is open
netstat -tulpn | grep :80

# Check dashboard
ps aux | grep gunicorn

# Check files
ls -la /var/www/rafael/
```

### From Your Computer
```bash
# Test direct IP
curl http://154.19.37.180

# Test domain (after DNS)
curl http://rafaelabs.xyz

# Check DNS
nslookup rafaelabs.xyz
```

---

## 🆘 Troubleshooting

### Can't Connect via SSH
```powershell
# Test connection
Test-NetConnection -ComputerName 154.19.37.180 -Port 22

# Try with verbose
ssh -v root@154.19.37.180
```

### Upload Fails
```powershell
# Make sure PuTTY is installed
where pscp

# Try with full path
"C:\Program Files\PuTTY\pscp.exe" -pw "fM9e%gxZnJQ8" file.txt root@154.19.37.180:/root/
```

### Nginx Not Starting
```bash
# Check configuration
nginx -t

# Check logs
tail -f /var/log/nginx/error.log

# Check if port is in use
netstat -tulpn | grep :80
```

### Dashboard Not Working
```bash
# Check if Python is installed
python3.11 --version

# Check if RAFAEL is installed
python3.11 -c "import rafael; print(rafael.__version__)"

# Check dashboard files
ls -la /var/www/rafael/dashboard/
```

---

## 📝 Summary

### What You Need to Do:
1. ✅ Choose upload method (WinSCP recommended)
2. ✅ Upload files to server
3. ✅ Run deployment script
4. ✅ Wait for DNS propagation (24-48 hours)
5. ✅ Setup SSL certificates
6. ✅ Test all services

### Files to Upload:
- `dashboard/` → `/var/www/rafael/dashboard/`
- `beta/` → `/var/www/rafael/beta/`
- `examples/` → `/var/www/rafael/examples/`
- `deploy_to_server.sh` → `/root/`

### Expected Timeline:
- Upload files: 10-30 minutes
- Run deployment: 5-10 minutes
- DNS propagation: 24-48 hours
- SSL setup: 5 minutes
- **Total**: 2-3 days (mostly waiting for DNS)

---

**🔱 RAFAEL Framework**  
*Ready to deploy to rafaelabs.xyz*

**Server**: 154.19.37.180 ✅  
**Files**: Ready to upload  
**Guide**: Complete
