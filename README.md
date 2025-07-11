# PDF Reports Management System

A modern web-based PDF management system that allows you to organize, search, and view PDF files from local directories with advanced filtering and search capabilities.

![PDF Reports System](https://img.shields.io/badge/Status-Production%20Ready-green) ![Python](https://img.shields.io/badge/Python-3.11+-blue) ![React](https://img.shields.io/badge/React-19.0+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green)

## 🌟 Features

- **📁 Folder-Based Organization**: Automatically organizes PDFs from sub-folders
- **🔍 Advanced Search**: Search by filename and full PDF content
- **📅 Date Filtering**: Filter PDFs by creation/modification date
- **📄 PDF Viewer**: Built-in PDF viewer with responsive design
- **⚡ Real-time Updates**: Live search and filtering
- **📱 Responsive Design**: Works on desktop, tablet, and mobile
- **🎨 Modern UI**: Clean, professional interface with Tailwind CSS

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your Windows PC:

### Required Software

1. **Python 3.11 or higher**
   - Download from: https://www.python.org/downloads/
   - ⚠️ **Important**: During installation, check "Add Python to PATH"

2. **Node.js 18 or higher**
   - Download from: https://nodejs.org/
   - This includes npm (Node Package Manager)

3. **Git** (optional, for version control)
   - Download from: https://git-scm.com/download/win

4. **MongoDB** (for data storage)
   - Download from: https://www.mongodb.com/try/download/community
   - Or use MongoDB Atlas (cloud) for easier setup

### Framework Versions Used

- **FastAPI**: 0.110.1+ (uses modern lifespan event handlers)
- **React**: 19.0+
- **PyMuPDF**: 1.23.0+ (for PDF processing)
- **Tailwind CSS**: 3.4.17+ (for styling)

### Verify Installation

Open Command Prompt (cmd) or PowerShell and run:

```bash
python --version          # Should show Python 3.11+
node --version            # Should show Node.js 18+
npm --version             # Should show npm version
```

## 🚀 Installation Guide for Windows

### Step 1: Download the Project

Option A: **Download as ZIP**
1. Download the project files to your computer
2. Extract to a folder like `C:\pdf-reports-system`

Option B: **Clone with Git** (if you have Git installed)
```bash
git clone <repository-url>
cd pdf-reports-system
```

### Step 2: Set Up Python Environment

1. **Open Command Prompt or PowerShell as Administrator**

2. **Navigate to the project directory:**
```bash
cd C:\path\to\your\pdf-reports-system
```

3. **Create a virtual environment:**
```bash
python -m venv venv
```

4. **Activate the virtual environment:**
```bash
# For Command Prompt:
venv\Scripts\activate

# For PowerShell:
venv\Scripts\Activate.ps1
```

5. **Install Python dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Set Up Frontend

1. **Navigate to frontend directory:**
```bash
cd ..\frontend
```

2. **Install Node.js dependencies:**
```bash
npm install
# or
yarn install
```

### Step 4: Set Up MongoDB

#### Option A: Local MongoDB Installation

1. **Install MongoDB Community Server**
   - Download and install from MongoDB website
   - Start MongoDB service:
   ```bash
   net start MongoDB
   ```

2. **Verify MongoDB is running:**
   - Open browser and go to `http://localhost:27017`
   - You should see "It looks like you are trying to access MongoDB over HTTP"

#### Option B: MongoDB Atlas (Cloud - Recommended for beginners)

1. **Create free account at** https://cloud.mongodb.com/
2. **Create a new cluster**
3. **Get connection string** and update in backend/.env file

### Step 5: Configure Environment Variables

1. **Backend Configuration** (`backend/.env`):
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="pdf_reports_db"
```

2. **Frontend Configuration** (`frontend/.env`):
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

### Step 6: Create Reports Directory

1. **Create reports folder in project root:**
```bash
mkdir reports
```

2. **Create sample sub-folders:**
```bash
mkdir reports\financial_reports
mkdir reports\project_updates
mkdir reports\technical_docs
mkdir reports\hr_documents
mkdir reports\marketing_analytics
```

3. **Add your PDF files** to these sub-folders, or run the sample data generator:
```bash
cd scripts
python create_sample_pdfs.py
```

## 🏃‍♂️ Running the Application

### Method 1: Manual Start (Recommended for Development)

1. **Start the Backend Server:**
```bash
# Open new Command Prompt/PowerShell
cd C:\path\to\your\pdf-reports-system\backend
venv\Scripts\activate
python server.py
```
Backend will run on: http://localhost:8001

2. **Start the Frontend Server:**
```bash
# Open another Command Prompt/PowerShell
cd C:\path\to\your\pdf-reports-system\frontend
npm start
```
Frontend will run on: http://localhost:3000

3. **Open your browser** and go to: http://localhost:3000

### Method 2: Using Scripts (Advanced)

Create batch files for easier startup:

**start_backend.bat:**
```batch
@echo off
cd /d "C:\path\to\your\pdf-reports-system\backend"
call venv\Scripts\activate
python server.py
pause
```

**start_frontend.bat:**
```batch
@echo off
cd /d "C:\path\to\your\pdf-reports-system\frontend"
npm start
pause
```

## 📚 Usage Guide

### Adding PDF Files

1. **Organize your PDFs** into sub-folders within the `reports` directory:
   ```
   reports/
   ├── financial_reports/
   │   ├── Q1_Report.pdf
   │   └── Budget_2024.pdf
   ├── project_updates/
   │   └── Project_Alpha.pdf
   └── technical_docs/
       └── API_Documentation.pdf
   ```

2. **Supported formats**: .pdf files only

3. **File naming**: Use descriptive names for better search results

### Using the Interface

1. **Browse Folders**: Click on folder tabs in the left sidebar
2. **Select PDFs**: Click on PDF names to view them
3. **Search**: Type in the search box to find PDFs by name or content
4. **Date Filter**: Use the date/time picker to filter by modification date
5. **View PDFs**: Selected PDFs display in the main viewer area

### Search Tips

- **Filename search**: Type part of the filename
- **Content search**: Type any text that might be inside the PDFs
- **Combine terms**: Use multiple keywords for better results
- **Date filtering**: Adjust the target date to see only relevant PDFs

## 🛠️ Troubleshooting

### Common Issues

#### 1. "Python not found" error
**Solution**: Ensure Python is installed and added to PATH
```bash
# Check if Python is accessible
python --version
```

#### 2. "Module not found" errors
**Solution**: Ensure virtual environment is activated and dependencies installed
```bash
# Activate virtual environment
venv\Scripts\activate
# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Frontend won't start
**Solution**: Clear npm cache and reinstall
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### 4. MongoDB connection issues
**Solution**: 
- Check if MongoDB service is running: `net start MongoDB`
- Verify connection string in `.env` file
- For Atlas: ensure IP whitelist includes your IP

#### 5. PDFs not loading
**Solution**:
- Check file permissions on reports folder
- Ensure PDFs are not corrupted
- Verify backend is running on correct port (8001)

#### 6. Search not working
**Solution**:
- Ensure PyMuPDF is installed: `pip install PyMuPDF`
- Check backend logs for PDF processing errors
- Verify PDFs contain searchable text (not scanned images)

### Logs and Debugging

**Backend logs**: Check console where you started the backend server
**Frontend logs**: Check browser Developer Tools (F12) → Console
**MongoDB logs**: Check MongoDB log files in installation directory

## 📁 Project Structure

```
pdf-reports-system/
├── backend/                 # FastAPI backend
│   ├── server.py           # Main server file
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Backend configuration
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   ├── App.css        # Styles
│   │   └── index.js       # Entry point
│   ├── package.json       # Node.js dependencies
│   └── .env              # Frontend configuration
├── reports/               # PDF storage directory
│   ├── financial_reports/
│   ├── project_updates/
│   ├── technical_docs/
│   ├── hr_documents/
│   └── marketing_analytics/
├── scripts/               # Utility scripts
│   └── create_sample_pdfs.py
└── README.md             # This file
```

## 🔧 Configuration Options

### Backend Configuration (backend/.env)

```env
# Database settings
MONGO_URL="mongodb://localhost:27017"
DB_NAME="pdf_reports_db"

# Server settings (optional)
HOST="localhost"
PORT=8001
DEBUG=True
```

### Frontend Configuration (frontend/.env)

```env
# Backend API URL
REACT_APP_BACKEND_URL=http://localhost:8001

# Development settings
GENERATE_SOURCEMAP=false
BROWSER=none
```

## 🚀 Deployment for Production

### For Windows Server

1. **Install IIS with Application Request Routing (ARR)**
2. **Configure reverse proxy** to route requests
3. **Set up Windows Service** for backend
4. **Build frontend for production:**
```bash
npm run build
```
5. **Serve frontend** through IIS

### For Cloud Deployment

1. **Backend**: Deploy to services like Azure App Service, AWS EC2
2. **Frontend**: Build and deploy to Azure Static Web Apps, Netlify, or Vercel
3. **Database**: Use MongoDB Atlas for cloud database

## 📝 Adding New Features

### Adding New Folder Types

1. Create new sub-folder in `reports` directory
2. Add PDFs to the new folder
3. System will automatically detect and display

### Customizing Search

Modify the search functionality in:
- Backend: `server.py` → `search_pdfs()` function
- Frontend: `App.js` → search handling logic

### Styling Changes

Modify styles in:
- `frontend/src/App.css` for custom styles
- Tailwind classes in `frontend/src/App.js` for utility-based styling

## 🔒 Security Considerations

- **File Access**: System only serves files from the reports directory
- **Input Validation**: All user inputs are validated on the backend
- **CORS**: Configure CORS settings for production deployment
- **Environment Variables**: Keep sensitive data in .env files
- **PDF Processing**: Uses secure PyMuPDF library for PDF operations

## 📞 Support

For issues or questions:

1. **Check this README** for common solutions
2. **Review error logs** in console/terminal
3. **Verify all prerequisites** are installed correctly
4. **Test with sample data** to isolate issues

## 🎯 Performance Tips

1. **Organize PDFs**: Keep reasonable number of PDFs per folder (< 1000)
2. **File Sizes**: Optimize PDF file sizes for better loading
3. **Search**: Use specific search terms for faster results
4. **Hardware**: Ensure adequate RAM for large PDF processing

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📝 Changelog

### Version 1.1.0 (Latest)
- ✅ **Fixed**: Updated FastAPI to use modern lifespan event handlers instead of deprecated `on_event`
- ✅ **Improved**: Better error handling and logging during startup/shutdown
- ✅ **Enhanced**: More detailed Windows deployment documentation

### Version 1.0.0 (Initial Release)
- ✅ **Feature**: Complete PDF management system with folder organization
- ✅ **Feature**: Advanced search functionality (filename + content)
- ✅ **Feature**: Date/time filtering based on PDF metadata
- ✅ **Feature**: Built-in PDF viewer with responsive design
- ✅ **Feature**: Windows deployment scripts and documentation

---

**Happy PDF Management! 🎉**

For the best experience, ensure your reports folder is well-organized and your PDFs contain searchable text content.
