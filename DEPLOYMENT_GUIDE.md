# DEPLOYMENT_GUIDE.md

# Windows Deployment Guide for PDF Reports Management System

## Quick Start (5 Minutes Setup)

### Method 1: Automated Setup (Recommended)

1. **Download the project** and extract to `C:\pdf-reports-system`

2. **Run the setup script** as Administrator:
   ```bash
   # Right-click on Command Prompt → "Run as administrator"
   cd C:\pdf-reports-system
   setup_windows.bat
   ```

3. **Start the application**:
   - Double-click `start_backend.bat`
   - Double-click `start_frontend.bat` (in a new window)
   - Open http://localhost:3000 in your browser

### Method 2: Manual Setup

Follow the detailed instructions in the main README.md file.

## Production Deployment on Windows Server

### Option 1: IIS + Windows Services

#### Step 1: Prepare the Application

1. **Build React app for production**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Create Windows Service for Backend**:
   ```bash
   # Install Python service wrapper
   pip install pywin32
   
   # Create service script (create as backend_service.py)
   ```

#### Step 2: Configure IIS

1. **Install IIS and URL Rewrite Module**
2. **Create website pointing to frontend/build**
3. **Configure reverse proxy for API calls**

#### Step 3: Set up Backend Service

1. **Install backend as Windows Service**
2. **Configure service to start automatically**
3. **Set up service monitoring**

### Option 2: Docker Deployment

#### Step 1: Create Dockerfiles

**Backend Dockerfile** (create in backend/):
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["python", "server.py"]
```

**Frontend Dockerfile** (create in frontend/):
```dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
```

#### Step 2: Docker Compose

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8001:8001"
    environment:
      - MONGO_URL=mongodb://mongodb:27017
      - DB_NAME=pdf_reports_db
    volumes:
      - ./reports:/app/reports
    depends_on:
      - mongodb

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  mongodb:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

#### Step 3: Deploy with Docker

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Environment Configuration

### Development Environment

**backend/.env**:
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="pdf_reports_dev"
DEBUG=True
HOST="localhost"
PORT=8001
```

**frontend/.env**:
```env
REACT_APP_BACKEND_URL=http://localhost:8001
GENERATE_SOURCEMAP=true
```

### Production Environment

**backend/.env**:
```env
MONGO_URL="mongodb://production-server:27017"
DB_NAME="pdf_reports_prod"
DEBUG=False
HOST="0.0.0.0"
PORT=8001
```

**frontend/.env**:
```env
REACT_APP_BACKEND_URL=https://your-domain.com/api
GENERATE_SOURCEMAP=false
```

## Security Configuration

### 1. Firewall Rules

```bash
# Allow HTTP traffic
netsh advfirewall firewall add rule name="PDF Reports HTTP" dir=in action=allow protocol=TCP localport=80

# Allow HTTPS traffic
netsh advfirewall firewall add rule name="PDF Reports HTTPS" dir=in action=allow protocol=TCP localport=443
```

### 2. SSL Certificate Setup

1. **Obtain SSL certificate** from Let's Encrypt or commercial CA
2. **Configure IIS** to use SSL certificate
3. **Update frontend .env** to use HTTPS URLs

### 3. Access Control

1. **Windows Authentication** integration
2. **File system permissions** for reports folder
3. **Database access** restrictions

## Monitoring and Maintenance

### 1. Log Management

**Backend Logs**:
- Location: `backend/logs/`
- Rotation: Daily
- Retention: 30 days

**IIS Logs**:
- Location: `C:\inetpub\logs\LogFiles\`
- Format: W3C Extended

### 2. Health Checks

Create `health_check.ps1`:
```powershell
# Check backend service
$backend = Test-NetConnection -ComputerName localhost -Port 8001
if (-not $backend.TcpTestSucceeded) {
    Write-Host "Backend service is down" -ForegroundColor Red
    # Restart service logic here
}

# Check frontend
$frontend = Test-NetConnection -ComputerName localhost -Port 80
if (-not $frontend.TcpTestSucceeded) {
    Write-Host "Frontend service is down" -ForegroundColor Red
    # Restart IIS logic here
}

# Check MongoDB
$mongo = Test-NetConnection -ComputerName localhost -Port 27017
if (-not $mongo.TcpTestSucceeded) {
    Write-Host "MongoDB is down" -ForegroundColor Red
    # Restart MongoDB logic here
}
```

### 3. Backup Strategy

**Database Backup**:
```bash
# Daily MongoDB backup
mongodump --host localhost:27017 --db pdf_reports_prod --out backup/$(date +%Y%m%d)
```

**Files Backup**:
```bash
# Backup reports folder
robocopy "C:\pdf-reports-system\reports" "D:\backups\reports" /MIR /XA:SH /W:5
```

## Performance Optimization

### 1. Backend Optimization

- **Gunicorn** for production ASGI server
- **Connection pooling** for MongoDB
- **Caching** for frequently accessed PDFs
- **Load balancing** for multiple instances

### 2. Frontend Optimization

- **CDN** for static assets
- **Gzip compression** in IIS
- **Browser caching** headers
- **Code splitting** for React components

### 3. Database Optimization

- **Indexes** on frequently queried fields
- **Connection limits** configuration
- **Memory allocation** tuning

## Troubleshooting Production Issues

### Common Production Problems

1. **Service Won't Start**
   - Check Windows Event Log
   - Verify file permissions
   - Check port conflicts

2. **High Memory Usage**
   - Monitor PDF processing
   - Check for memory leaks
   - Adjust connection limits

3. **Slow Performance**
   - Enable performance counters
   - Check disk I/O
   - Monitor network latency

### Diagnostic Commands

```bash
# Check service status
sc query "PDF Reports Backend"

# Check port usage
netstat -an | findstr :8001

# Check process memory
tasklist /fi "imagename eq python.exe" /fo table

# Check disk space
dir C:\ /-c
```

## Scaling Considerations

### Horizontal Scaling

1. **Load Balancer** (IIS ARR or F5)
2. **Multiple Backend Instances**
3. **Shared File Storage** (NFS or SMB)
4. **Database Clustering**

### Vertical Scaling

1. **Increase RAM** for PDF processing
2. **Faster Storage** (SSD) for better I/O
3. **More CPU Cores** for concurrent processing

## Backup and Recovery

### 1. Automated Backup Script

Create `backup.ps1`:
```powershell
$date = Get-Date -Format "yyyyMMdd"
$backupPath = "D:\backups\$date"

# Create backup directory
New-Item -ItemType Directory -Path $backupPath -Force

# Backup database
& mongodump --host localhost:27017 --db pdf_reports_prod --out "$backupPath\database"

# Backup files
robocopy "C:\pdf-reports-system\reports" "$backupPath\reports" /MIR

# Backup configuration
Copy-Item "C:\pdf-reports-system\backend\.env" "$backupPath\backend.env"
Copy-Item "C:\pdf-reports-system\frontend\.env" "$backupPath\frontend.env"

Write-Host "Backup completed: $backupPath"
```

### 2. Recovery Procedures

**Database Recovery**:
```bash
# Restore from backup
mongorestore --host localhost:27017 --db pdf_reports_prod backup/20241209/database/pdf_reports_prod
```

**File Recovery**:
```bash
# Restore reports folder
robocopy "D:\backups\20241209\reports" "C:\pdf-reports-system\reports" /MIR
```

This guide provides comprehensive deployment instructions for Windows environments, from development to production-ready setups.