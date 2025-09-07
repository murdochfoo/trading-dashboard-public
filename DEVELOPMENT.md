# 🚀 Trading Dashboard Development Workflow

## Overview

This repository uses a **GitFlow-inspired** workflow with automated CI/CD:

```
development → staging → main (production)
     ↓           ↓         ↓
  Local Dev   Staging   Live Site
```

## 📁 Directory Structure

```
/home/ib/
├── trading-dashboard-public/     # ❌ PRODUCTION - Do not edit directly!
└── trading-dashboard-dev/        # ✅ DEVELOPMENT - Work here
    ├── dev-server.py             # Local development server
    ├── .github/workflows/        # CI/CD pipeline
    ├── index.html               # Main dashboard file
    ├── dashboard_data.json      # Strategy data
    └── DEVELOPMENT.md          # This file
```

## 🛠️ Development Setup

### 1. Start Local Development Server
```bash
cd /home/ib/trading-dashboard-dev
python dev-server.py --port 8000

# Open browser to: http://localhost:8000
```

### 2. Make Changes
- Edit files in `/home/ib/trading-dashboard-dev/`
- Test locally at `http://localhost:8000`
- Refresh browser to see changes (no cache)

### 3. Git Workflow
```bash
# Always work on development branch
git checkout development

# Make your changes
git add .
git commit -m "feat: add new feature"

# Push to development
git push origin development
```

## 🚦 Deployment Process

### Development → Staging
```bash
# Create PR from development to staging
git checkout development
git push origin development

# Go to GitHub and create PR: development → staging
# CI/CD will run tests automatically
# After tests pass and PR approved, merge to staging
```

### Staging → Production  
```bash
# Create PR from staging to main
git checkout staging  
git push origin staging

# Go to GitHub and create PR: staging → main
# CI/CD will run full test suite + security scan
# After tests pass and PR approved, merge to main
# Site automatically deploys to: https://murdochfoo.github.io/trading-dashboard-public/
```

## 🧪 Testing & Validation

The CI/CD pipeline automatically runs:

### ✅ On Every Push/PR:
- **HTML Structure Validation**: Checks for required tags and structure
- **JSON Data Validation**: Verifies all required strategy data exists
- **Playwright Browser Tests**: Tests dashboard loading and functionality  
- **RAG Compliance Check**: Ensures realistic performance metrics

### ✅ On Production Deployment:
- **Security Scan**: Checks for sensitive information
- **Post-deployment Verification**: Confirms live site is accessible
- **Performance Check**: Validates site loads within acceptable time

## 🔒 Branch Protection Rules

### Main Branch (Production)
- ❌ **No direct pushes allowed**
- ✅ **Requires PR with 1+ approval**  
- ✅ **All CI tests must pass**
- ✅ **Security scan must pass**
- ✅ **Branch must be up-to-date**

### Staging Branch
- ❌ **No direct pushes allowed**
- ✅ **Requires PR with 1+ approval**
- ✅ **Tests must pass**

### Development Branch
- ✅ **Direct pushes allowed** (for development speed)
- ✅ **Tests run on push** (for early feedback)

## 📋 Development Commands

### Local Development
```bash
# Start development server
python dev-server.py

# Start on different port
python dev-server.py --port 3000

# Run tests locally (requires playwright)
python -c "import asyncio; from playwright.async_api import async_playwright; # ... test code"
```

### Git Operations
```bash
# Check current branch and status
git branch
git status

# Switch branches
git checkout development
git checkout staging

# Create feature branch (optional)
git checkout -b feature/new-dashboard-section

# View recent commits
git log --oneline -10

# View remote info
git remote -v
```

## 🚨 Emergency Procedures

### Production Hotfix
```bash
# For critical production issues
git checkout main
git checkout -b hotfix/critical-fix

# Make minimal fix
git add .
git commit -m "hotfix: fix critical production issue"

# Create PR directly to main
git push origin hotfix/critical-fix
```

### Rollback Production
```bash
# If production deployment fails
git checkout main
git reset --hard HEAD~1  # Go back one commit
git push --force-with-lease origin main
```

## 🔍 Debugging Common Issues

### Local Server Won't Start
```bash
# Check if port is in use
lsof -i :8000

# Kill process using port
kill $(lsof -t -i :8000)

# Try different port
python dev-server.py --port 8001
```

### CI/CD Tests Failing
1. **HTML Validation**: Check for malformed HTML tags
2. **JSON Validation**: Ensure `dashboard_data.json` is valid JSON
3. **Playwright Tests**: Test locally first with browser automation
4. **RAG Compliance**: Check that performance metrics are realistic

### Branch Protection Issues
- **Can't push to main**: Create PR instead
- **Tests required but not running**: Check GitHub Actions tab
- **PR can't merge**: Ensure all required tests pass

## 📊 Monitoring & Metrics

### CI/CD Pipeline Status
- **GitHub Actions**: `https://github.com/murdochfoo/trading-dashboard-public/actions`
- **Branch Protection**: `https://github.com/murdochfoo/trading-dashboard-public/settings/branches`

### Production Monitoring
- **Live Site**: `https://murdochfoo.github.io/trading-dashboard-public/`
- **GitHub Pages Status**: Repository → Settings → Pages

## 🎯 Best Practices

### Development
- ✅ **Always test locally** before pushing
- ✅ **Use descriptive commit messages**: `feat:`, `fix:`, `chore:`
- ✅ **Keep changes small and focused**
- ✅ **Document significant changes**

### Data Management
- ✅ **Validate JSON before committing**
- ✅ **Keep realistic performance metrics** (RAG compliant)
- ✅ **Test with full dataset** locally

### Security
- ❌ **Never commit sensitive information**
- ✅ **Use environment variables** for secrets
- ✅ **Keep repository public-safe**

## 🆘 Getting Help

### Quick Reference
- **Local dev server**: `python dev-server.py`
- **Current branch**: `git branch`
- **View changes**: `git status`
- **Test pipeline**: Push to `development` branch

### Troubleshooting Checklist
1. ✅ Are you on the right branch? (`git branch`)
2. ✅ Is the local server running? (`python dev-server.py`)
3. ✅ Are changes saved and committed? (`git status`)
4. ✅ Did CI/CD tests pass? (Check GitHub Actions)
5. ✅ Are branch protection rules being followed?

---

**Remember**: This new workflow prevents accidental production changes and ensures all code is tested before going live! 🎉