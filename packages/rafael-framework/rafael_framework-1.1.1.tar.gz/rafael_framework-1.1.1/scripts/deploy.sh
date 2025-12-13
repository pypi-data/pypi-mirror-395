#!/bin/bash
# RAFAEL Framework Deployment Script

set -e

echo "🔱 RAFAEL Framework Deployment Script"
echo "======================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    print_error "setup.py not found. Please run this script from the RAFAEL root directory."
    exit 1
fi

print_info "Starting deployment process..."

# 1. Clean previous builds
print_info "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info
print_success "Cleaned build directories"

# 2. Run tests
print_info "Running tests..."
if python -m pytest tests/ -v; then
    print_success "All tests passed"
else
    print_error "Tests failed. Aborting deployment."
    exit 1
fi

# 3. Build package
print_info "Building package..."
if python -m build; then
    print_success "Package built successfully"
else
    print_error "Build failed"
    exit 1
fi

# 4. Check distribution
print_info "Checking distribution..."
if python -m twine check dist/*; then
    print_success "Distribution check passed"
else
    print_error "Distribution check failed"
    exit 1
fi

# 5. Ask for confirmation
echo ""
print_info "Ready to upload to PyPI"
read -p "Do you want to continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Deployment cancelled"
    exit 0
fi

# 6. Upload to PyPI
print_info "Uploading to PyPI..."
if python -m twine upload dist/*; then
    print_success "Successfully uploaded to PyPI!"
else
    print_error "Upload failed"
    exit 1
fi

# 7. Build Docker image
print_info "Building Docker image..."
if docker build -t rafaelframework/rafael:latest .; then
    print_success "Docker image built successfully"
else
    print_error "Docker build failed"
    exit 1
fi

# 8. Tag Docker image
VERSION=$(python -c "import setup; print(setup.version)")
docker tag rafaelframework/rafael:latest rafaelframework/rafael:$VERSION
print_success "Docker image tagged as $VERSION"

# 9. Ask to push Docker image
echo ""
print_info "Ready to push Docker image"
read -p "Do you want to push to Docker Hub? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Pushing Docker image..."
    docker push rafaelframework/rafael:latest
    docker push rafaelframework/rafael:$VERSION
    print_success "Docker image pushed successfully"
fi

echo ""
print_success "🎉 Deployment completed successfully!"
echo ""
print_info "Next steps:"
echo "  1. Create GitHub release: git tag -a v$VERSION -m 'Release v$VERSION'"
echo "  2. Push tag: git push origin v$VERSION"
echo "  3. Announce on social media"
echo ""
