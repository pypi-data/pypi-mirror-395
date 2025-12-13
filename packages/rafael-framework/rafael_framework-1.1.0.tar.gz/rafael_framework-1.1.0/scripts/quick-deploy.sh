#!/bin/bash
# Quick deployment script for RAFAEL Framework
# This script handles the most common deployment scenario

set -e

echo "🔱 RAFAEL Quick Deploy"
echo "====================="
echo ""

# Check prerequisites
command -v python >/dev/null 2>&1 || { echo "❌ Python is required but not installed."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Git is required but not installed."; exit 1; }

# Step 1: Run tests
echo "1️⃣ Running tests..."
if python -m pytest tests/ -q; then
    echo "✅ Tests passed"
else
    echo "❌ Tests failed"
    exit 1
fi

# Step 2: Build package
echo ""
echo "2️⃣ Building package..."
rm -rf build/ dist/ *.egg-info
python -m build
echo "✅ Package built"

# Step 3: Git operations
echo ""
echo "3️⃣ Git operations..."
read -p "Commit message: " commit_msg
git add .
git commit -m "$commit_msg" || echo "Nothing to commit"
git push
echo "✅ Pushed to Git"

# Step 4: Optional - Deploy to PyPI
echo ""
read -p "Deploy to PyPI? (y/N): " deploy_pypi
if [[ $deploy_pypi =~ ^[Yy]$ ]]; then
    echo "4️⃣ Deploying to PyPI..."
    python -m twine upload dist/*
    echo "✅ Deployed to PyPI"
fi

echo ""
echo "🎉 Deployment complete!"
