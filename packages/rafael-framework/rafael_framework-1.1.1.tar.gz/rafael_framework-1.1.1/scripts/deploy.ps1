# RAFAEL Framework Deployment Script (PowerShell)
# For Windows users

$ErrorActionPreference = "Stop"

Write-Host "🔱 RAFAEL Framework Deployment Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

function Print-Success {
    param($Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Print-Error {
    param($Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Print-Info {
    param($Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Yellow
}

# Check if we're in the right directory
if (-not (Test-Path "setup.py")) {
    Print-Error "setup.py not found. Please run this script from the RAFAEL root directory."
    exit 1
}

Print-Info "Starting deployment process..."

# 1. Clean previous builds
Print-Info "Cleaning previous builds..."
Remove-Item -Path "build", "dist", "*.egg-info" -Recurse -Force -ErrorAction SilentlyContinue
Print-Success "Cleaned build directories"

# 2. Run tests
Print-Info "Running tests..."
try {
    python -m pytest tests/ -v
    Print-Success "All tests passed"
} catch {
    Print-Error "Tests failed. Aborting deployment."
    exit 1
}

# 3. Build package
Print-Info "Building package..."
try {
    python -m build
    Print-Success "Package built successfully"
} catch {
    Print-Error "Build failed"
    exit 1
}

# 4. Check distribution
Print-Info "Checking distribution..."
try {
    python -m twine check dist/*
    Print-Success "Distribution check passed"
} catch {
    Print-Error "Distribution check failed"
    exit 1
}

# 5. Ask for confirmation
Write-Host ""
Print-Info "Ready to upload to PyPI"
$confirmation = Read-Host "Do you want to continue? (y/N)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Print-Info "Deployment cancelled"
    exit 0
}

# 6. Upload to PyPI
Print-Info "Uploading to PyPI..."
try {
    python -m twine upload dist/*
    Print-Success "Successfully uploaded to PyPI!"
} catch {
    Print-Error "Upload failed"
    exit 1
}

# 7. Build Docker image
Print-Info "Building Docker image..."
try {
    docker build -t rafaelframework/rafael:latest .
    Print-Success "Docker image built successfully"
} catch {
    Print-Error "Docker build failed"
    exit 1
}

# 8. Tag Docker image
$version = python -c "import setup; print(setup.version)"
docker tag rafaelframework/rafael:latest "rafaelframework/rafael:$version"
Print-Success "Docker image tagged as $version"

# 9. Ask to push Docker image
Write-Host ""
Print-Info "Ready to push Docker image"
$confirmation = Read-Host "Do you want to push to Docker Hub? (y/N)"
if ($confirmation -eq 'y' -or $confirmation -eq 'Y') {
    Print-Info "Pushing Docker image..."
    docker push rafaelframework/rafael:latest
    docker push "rafaelframework/rafael:$version"
    Print-Success "Docker image pushed successfully"
}

Write-Host ""
Print-Success "🎉 Deployment completed successfully!"
Write-Host ""
Print-Info "Next steps:"
Write-Host "  1. Create GitHub release: git tag -a v$version -m 'Release v$version'"
Write-Host "  2. Push tag: git push origin v$version"
Write-Host "  3. Announce on social media"
Write-Host ""
