# Git Repository Setup and Push Instructions

## Quick Update (if repository already exists)

If you already have a GitHub repository set up, use these commands to push the latest fixes:

```bash
# Navigate to your project directory
cd C:\path\to\your\pdf-reports-system

# Add all changes
git add .

# Commit the fixes
git commit -m "Fix: Resolved environment variable KeyError and FastAPI deprecation warning

- Fixed KeyError for MONGO_URL and DB_NAME environment variables
- Added fallback defaults for missing environment variables
- Enhanced environment file loading with error handling
- Updated FastAPI to use modern lifespan event handlers
- Improved logging and MongoDB connection testing
- Added automatic reports directory creation
- Updated documentation with troubleshooting guide"

# Push to GitHub
git push origin main
```

## Step 1: Initialize Git Repository (if not already done)

```bash
# Navigate to your project directory
cd C:\path\to\your\pdf-reports-system

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: PDF Reports Management System"
```

## Step 2: Create GitHub Repository

1. **Go to GitHub.com** and sign in
2. **Click "New repository"** (green button)
3. **Name your repository**: `pdf-reports-management-system`
4. **Add description**: "A modern web-based PDF management system with search and filtering capabilities"
5. **Keep it Public** (or Private if preferred)
6. **Don't initialize** with README, .gitignore, or license (we already have these)
7. **Click "Create repository"**

## Step 3: Connect Local Repository to GitHub

```bash
# Add GitHub repository as remote origin
git remote add origin https://github.com/YOUR_USERNAME/pdf-reports-management-system.git

# Verify remote was added
git remote -v

# Push to GitHub
git push -u origin main
```

## Step 4: Alternative - Using GitHub Desktop

1. **Download GitHub Desktop** from https://desktop.github.com/
2. **Install and sign in** to your GitHub account
3. **Click "Add an Existing Repository from your Hard Drive"**
4. **Select your project folder**
5. **Click "Publish Repository"**
6. **Enter repository name** and click "Publish Repository"

## Step 5: Verify Repository

1. **Go to your GitHub repository** in browser
2. **Check that all files are present**:
   - README.md
   - DEPLOYMENT_GUIDE.md
   - backend/ folder
   - frontend/ folder
   - scripts/ folder
   - .bat files for Windows
3. **Verify README displays properly** with formatting

## Commands to Run

Here are the exact commands you need to run in Command Prompt or PowerShell:

```bash
# 1. Navigate to your project
cd C:\pdf-reports-system

# 2. Initialize git (if not done)
git init

# 3. Add all files
git add .

# 4. Commit files
git commit -m "Complete PDF Reports Management System with Windows deployment"

# 5. Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/pdf-reports-management-system.git

# 6. Push to GitHub
git push -u origin main
```

## If You Encounter Issues

### Issue 1: Authentication Error
**Solution**: Use Personal Access Token instead of password
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with repo permissions
3. Use token as password when prompted

### Issue 2: Repository Already Exists
**Solution**: Clone existing repository or use different name
```bash
# Check existing remotes
git remote -v

# Remove existing remote
git remote remove origin

# Add new remote with different name
git remote add origin https://github.com/YOUR_USERNAME/NEW_REPOSITORY_NAME.git
```

### Issue 3: Main vs Master Branch
**Solution**: Check default branch name
```bash
# Check current branch
git branch

# Rename branch if needed
git branch -M main

# Then push
git push -u origin main
```

## Repository Structure After Push

Your GitHub repository should contain:

```
pdf-reports-management-system/
├── README.md                    # Main documentation
├── DEPLOYMENT_GUIDE.md          # Windows deployment guide
├── setup_windows.bat            # Automated setup script
├── start_backend.bat            # Backend startup script
├── start_frontend.bat           # Frontend startup script
├── backend/                     # Python FastAPI backend
│   ├── server.py
│   ├── requirements.txt
│   └── .env
├── frontend/                    # React frontend
│   ├── src/
│   ├── package.json
│   └── .env
├── scripts/                     # Utility scripts
│   └── create_sample_pdfs.py
├── reports/                     # PDF storage (excluded from git)
└── .gitignore                   # Git ignore rules
```

## Next Steps After Repository Creation

1. **Add repository description** on GitHub
2. **Add topics/tags** for discoverability
3. **Create releases** for version management
4. **Set up GitHub Pages** for documentation (optional)
5. **Add contributing guidelines** (optional)
6. **Set up GitHub Actions** for CI/CD (optional)

Run these commands to complete the git setup!