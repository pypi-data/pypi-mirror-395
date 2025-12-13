# 🚀 RAFAEL Framework - Deployment Guide

Complete guide for deploying RAFAEL Framework to production.

---

## 📋 Prerequisites

### Required Tools
- Python 3.8+ installed
- Git installed
- Docker installed (for containerization)
- GitHub account
- PyPI account (for package distribution)
- Docker Hub account (optional)

### Required Credentials
- PyPI API token
- GitHub personal access token
- Docker Hub credentials (optional)

---

## 🔧 Setup

### 1. Install Build Tools

```bash
# Install build dependencies
pip install --upgrade pip
pip install build twine wheel setuptools

# Verify installation
python -m build --version
twine --version
```

### 2. Configure PyPI Credentials

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN-HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TEST-API-TOKEN-HERE
```

**Get PyPI Token:**
1. Go to https://pypi.org/manage/account/token/
2. Create new API token
3. Copy and paste to `.pypirc`

---

## 📦 Method 1: PyPI Deployment

### A. Test on TestPyPI First

```bash
# 1. Clean previous builds
rm -rf build/ dist/ *.egg-info

# 2. Build package
python -m build

# 3. Check distribution
twine check dist/*

# 4. Upload to TestPyPI
twine upload --repository testpypi dist/*

# 5. Test installation
pip install --index-url https://test.pypi.org/simple/ rafael-framework
```

### B. Deploy to Production PyPI

```bash
# 1. Build package
python -m build

# 2. Upload to PyPI
twine upload dist/*

# 3. Verify installation
pip install rafael-framework
rafael --version
```

### C. Using Deployment Script

**Linux/Mac:**
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

**Windows:**
```powershell
.\scripts\deploy.ps1
```

---

## 🐳 Method 2: Docker Deployment

### A. Build Docker Image

```bash
# Build image
docker build -t rafaelframework/rafael:latest .

# Tag with version
docker tag rafaelframework/rafael:latest rafaelframework/rafael:1.0.0

# Test locally
docker run -p 8080:8080 rafaelframework/rafael:latest
```

### B. Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Push images
docker push rafaelframework/rafael:latest
docker push rafaelframework/rafael:1.0.0
```

### C. Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f rafael

# Stop services
docker-compose down
```

---

## 🌐 Method 3: GitHub Repository

### A. Initialize Git Repository

```bash
# Initialize git
cd R:/RAFAEL
git init

# Add all files
git add .

# Initial commit
git commit -m "🔱 Initial commit: RAFAEL Framework v1.0.0"
```

### B. Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/Rafael2022-prog/rafael.git

# Push to main branch
git branch -M main
git push -u origin main
```

### C. Create Release

```bash
# Create and push tag
git tag -a v1.0.0 -m "RAFAEL Framework v1.0.0 - Production Release"
git push origin v1.0.0

# Or create release on GitHub UI:
# 1. Go to repository
# 2. Click "Releases"
# 3. Click "Create a new release"
# 4. Fill in details and publish
```

---

## ⚙️ Method 4: CI/CD with GitHub Actions

### Setup Secrets

1. Go to GitHub repository settings
2. Navigate to Secrets and variables → Actions
3. Add the following secrets:

```
PYPI_API_TOKEN          # Your PyPI token
DOCKER_USERNAME         # Docker Hub username
DOCKER_PASSWORD         # Docker Hub password
```

### Automatic Deployment

GitHub Actions will automatically:
- ✅ Run tests on every push
- ✅ Build package on every commit
- ✅ Deploy to PyPI on release
- ✅ Build and push Docker image

**Trigger deployment:**
```bash
# Create and push tag
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin v1.0.1

# GitHub Actions will automatically deploy
```

---

## 🚀 Method 5: Cloud Deployment

### A. AWS Elastic Container Service (ECS)

```bash
# 1. Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag rafaelframework/rafael:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/rafael:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/rafael:latest

# 2. Deploy to ECS
aws ecs update-service --cluster rafael-cluster --service rafael-service --force-new-deployment
```

### B. Google Cloud Run

```bash
# 1. Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT-ID/rafael

# 2. Deploy to Cloud Run
gcloud run deploy rafael \
  --image gcr.io/PROJECT-ID/rafael \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### C. Azure Container Instances

```bash
# 1. Login to Azure
az login

# 2. Create container
az container create \
  --resource-group rafael-rg \
  --name rafael-container \
  --image rafaelframework/rafael:latest \
  --dns-name-label rafael-framework \
  --ports 8080
```

### D. Kubernetes

```yaml
# rafael-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rafael
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rafael
  template:
    metadata:
      labels:
        app: rafael
    spec:
      containers:
      - name: rafael
        image: rafaelframework/rafael:latest
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: rafael-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: rafael
```

```bash
# Deploy to Kubernetes
kubectl apply -f rafael-deployment.yaml
```

---

## 🔍 Verification

### After Deployment

```bash
# 1. Verify PyPI package
pip install rafael-framework
rafael --version
rafael status

# 2. Verify Docker image
docker pull rafaelframework/rafael:latest
docker run -p 8080:8080 rafaelframework/rafael:latest

# 3. Run tests
python -m pytest tests/ -v

# 4. Check examples
python examples/fintech_example.py
python examples/game_example.py
```

---

## 📊 Monitoring

### Health Checks

```bash
# Docker health check
docker inspect --format='{{.State.Health.Status}}' rafael-container

# HTTP health check
curl http://localhost:8080/health

# Python health check
python -c "import core; print('healthy')"
```

### Logs

```bash
# Docker logs
docker logs -f rafael-container

# Docker Compose logs
docker-compose logs -f rafael

# Kubernetes logs
kubectl logs -f deployment/rafael
```

---

## 🐛 Troubleshooting

### Build Fails

```bash
# Clean and rebuild
rm -rf build/ dist/ *.egg-info
python -m build

# Check for errors
python setup.py check
```

### Upload Fails

```bash
# Check credentials
cat ~/.pypirc

# Test with TestPyPI first
twine upload --repository testpypi dist/*

# Verbose mode
twine upload --verbose dist/*
```

### Docker Issues

```bash
# Rebuild without cache
docker build --no-cache -t rafaelframework/rafael:latest .

# Check logs
docker logs rafael-container

# Interactive debugging
docker run -it rafaelframework/rafael:latest /bin/bash
```

---

## 📝 Checklist

Before deploying to production:

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Code is formatted (`black .`)
- [ ] Documentation is updated
- [ ] Version number is bumped
- [ ] CHANGELOG is updated
- [ ] LICENSE is correct
- [ ] README is accurate
- [ ] Examples work correctly
- [ ] Docker image builds successfully
- [ ] Security scan passed
- [ ] Performance benchmarks met

---

## 🔐 Security

### Best Practices

1. **Never commit credentials**
   - Use `.gitignore`
   - Use environment variables
   - Use secrets management

2. **Use API tokens**
   - Not passwords
   - Scope appropriately
   - Rotate regularly

3. **Scan for vulnerabilities**
   ```bash
   # Python dependencies
   pip install safety
   safety check
   
   # Docker image
   docker scan rafaelframework/rafael:latest
   ```

---

## 📞 Support

If you encounter issues:

1. Check [Troubleshooting](#troubleshooting) section
2. Review [GitHub Issues](https://github.com/Rafael2022-prog/rafael/issues)
3. Contact: info@rafael-framework.io

---

## 🎉 Post-Deployment

After successful deployment:

1. ✅ Announce on social media
2. ✅ Update documentation website
3. ✅ Write blog post
4. ✅ Create demo video
5. ✅ Notify community
6. ✅ Monitor metrics

---

**Congratulations! RAFAEL Framework is now deployed! 🔱**
