# RAFAEL Framework - Upload to Server Script
# PowerShell script untuk upload files ke server

$SERVER = "154.19.37.180"
$USERNAME = "root"
$PASSWORD = "fM9e%gxZnJQ8"

Write-Host "=========================================="
Write-Host "RAFAEL Framework - Upload to Server"
Write-Host "=========================================="
Write-Host ""

# Check if pscp (PuTTY SCP) is available
if (!(Get-Command pscp -ErrorAction SilentlyContinue)) {
    Write-Host "Installing PuTTY (includes pscp)..."
    winget install -e --id PuTTY.PuTTY
}

Write-Host "Uploading files to server..."
Write-Host ""

# Create temporary directory structure on server
Write-Host "1. Creating directories on server..."
$commands = @"
mkdir -p /var/www/rafael/dashboard
mkdir -p /var/www/rafael/beta
mkdir -p /var/www/rafael/landing
mkdir -p /var/www/rafael/docs
"@

echo $commands | plink -batch -pw $PASSWORD ${USERNAME}@${SERVER}

# Upload Dashboard files
Write-Host "2. Uploading Dashboard files..."
pscp -batch -pw $PASSWORD -r dashboard/* ${USERNAME}@${SERVER}:/var/www/rafael/dashboard/

# Upload Beta page
Write-Host "3. Uploading Beta page..."
pscp -batch -pw $PASSWORD -r beta/* ${USERNAME}@${SERVER}:/var/www/rafael/beta/

# Upload deployment script
Write-Host "4. Uploading deployment script..."
pscp -batch -pw $PASSWORD deploy_to_server.sh ${USERNAME}@${SERVER}:/root/

# Make deployment script executable and run it
Write-Host "5. Running deployment script on server..."
$deployCommands = @"
chmod +x /root/deploy_to_server.sh
/root/deploy_to_server.sh
"@

echo $deployCommands | plink -batch -pw $PASSWORD ${USERNAME}@${SERVER}

Write-Host ""
Write-Host "=========================================="
Write-Host "Upload Complete!"
Write-Host "=========================================="
Write-Host ""
Write-Host "Server is now configured with:"
Write-Host "- Nginx web server"
Write-Host "- Python 3.11"
Write-Host "- RAFAEL Framework"
Write-Host "- Dashboard at /var/www/rafael/dashboard"
Write-Host "- Beta page at /var/www/rafael/beta"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Wait for DNS propagation"
Write-Host "2. Setup SSL: ssh root@154.19.37.180"
Write-Host "   Then run: sudo certbot --nginx -d rafaelabs.xyz -d www.rafaelabs.xyz"
Write-Host "3. Start dashboard: sudo systemctl start rafael-dashboard"
Write-Host ""
Write-Host "Access your sites:"
Write-Host "- http://154.19.37.180 (direct IP)"
Write-Host "- http://rafaelabs.xyz (after DNS)"
Write-Host "- http://dashboard.rafaelabs.xyz (after DNS)"
Write-Host ""
