from fastapi import FastAPI, APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, time
import fitz  # PyMuPDF
import json
import re


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Reports directory
REPORTS_DIR = Path("/app/reports")

# Models
class PDFInfo(BaseModel):
    filename: str
    filepath: str
    folder: str
    size: int
    created_date: datetime
    modified_date: datetime
    text_content: str = ""

class FolderInfo(BaseModel):
    name: str
    pdf_count: int
    pdfs: List[PDFInfo]

class SearchResult(BaseModel):
    pdf: PDFInfo
    matches: List[str]
    match_count: int

# Helper functions
def extract_pdf_metadata_and_text(pdf_path: Path) -> Dict[str, Any]:
    """Extract metadata and text content from PDF"""
    try:
        # Get file stats
        stat = pdf_path.stat()
        created_date = datetime.fromtimestamp(stat.st_ctime)
        modified_date = datetime.fromtimestamp(stat.st_mtime)
        
        # Extract text content using PyMuPDF
        text_content = ""
        try:
            doc = fitz.open(str(pdf_path))
            for page in doc:
                text_content += page.get_text()
            doc.close()
        except Exception as e:
            logger.warning(f"Could not extract text from {pdf_path}: {e}")
            text_content = ""
        
        return {
            "filename": pdf_path.name,
            "filepath": str(pdf_path),
            "folder": pdf_path.parent.name,
            "size": stat.st_size,
            "created_date": created_date,
            "modified_date": modified_date,
            "text_content": text_content.strip()
        }
    except Exception as e:
        logger.error(f"Error processing {pdf_path}: {e}")
        return None

def scan_reports_directory() -> Dict[str, List[PDFInfo]]:
    """Scan reports directory and organize PDFs by folder"""
    folders = {}
    
    if not REPORTS_DIR.exists():
        logger.warning(f"Reports directory {REPORTS_DIR} does not exist")
        return folders
    
    for folder_path in REPORTS_DIR.iterdir():
        if folder_path.is_dir():
            folder_name = folder_path.name
            pdfs = []
            
            for pdf_path in folder_path.glob("*.pdf"):
                pdf_data = extract_pdf_metadata_and_text(pdf_path)
                if pdf_data:
                    pdfs.append(PDFInfo(**pdf_data))
            
            folders[folder_name] = pdfs
    
    return folders

def filter_pdfs_by_date(pdfs: List[PDFInfo], target_datetime: datetime) -> List[PDFInfo]:
    """Filter PDFs based on target datetime"""
    # Ensure both datetimes are naive for comparison
    # Convert target_datetime to naive if it's aware
    if target_datetime.tzinfo is not None:
        target_datetime = target_datetime.replace(tzinfo=None)
    
    return [
        pdf for pdf in pdfs 
        if pdf.modified_date.replace(tzinfo=None) <= target_datetime
    ]

def search_pdfs(pdfs: List[PDFInfo], search_term: str) -> List[SearchResult]:
    """Search PDFs by filename and content"""
    if not search_term.strip():
        return []
    
    results = []
    search_term_lower = search_term.lower()
    
    for pdf in pdfs:
        matches = []
        match_count = 0
        
        # Search in filename
        if search_term_lower in pdf.filename.lower():
            matches.append(f"Filename: {pdf.filename}")
            match_count += 1
        
        # Search in content
        if pdf.text_content:
            content_lower = pdf.text_content.lower()
            if search_term_lower in content_lower:
                # Find sentence containing the search term
                sentences = re.split(r'[.!?]+', pdf.text_content)
                for sentence in sentences:
                    if search_term_lower in sentence.lower():
                        # Truncate long sentences
                        if len(sentence) > 200:
                            # Find the position of search term and show context
                            pos = sentence.lower().find(search_term_lower)
                            start = max(0, pos - 100)
                            end = min(len(sentence), pos + 100)
                            context = sentence[start:end].strip()
                            if start > 0:
                                context = "..." + context
                            if end < len(sentence):
                                context = context + "..."
                        else:
                            context = sentence.strip()
                        
                        if context and len(context) > 10:
                            matches.append(f"Content: {context}")
                            match_count += 1
                        
                        # Limit to 3 content matches per PDF
                        if len([m for m in matches if m.startswith("Content:")]) >= 3:
                            break
        
        if matches:
            results.append(SearchResult(
                pdf=pdf,
                matches=matches,
                match_count=match_count
            ))
    
    # Sort by relevance (match count, then by filename)
    results.sort(key=lambda x: (-x.match_count, x.pdf.filename))
    return results

# API Routes
@api_router.get("/")
async def root():
    return {"message": "PDF Reports Management API"}

@api_router.get("/folders", response_model=List[FolderInfo])
async def get_folders(target_datetime: Optional[str] = None):
    """Get all folders with their PDFs, optionally filtered by target datetime"""
    try:
        folders_data = scan_reports_directory()
        result = []
        
        # Parse target datetime if provided
        filter_datetime = None
        if target_datetime:
            try:
                filter_datetime = datetime.fromisoformat(target_datetime.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid datetime format")
        else:
            # Default to today 11:59:59 PM
            today = datetime.now().date()
            filter_datetime = datetime.combine(today, time(23, 59, 59))
        
        for folder_name, pdfs in folders_data.items():
            # Filter PDFs by date if specified
            filtered_pdfs = filter_pdfs_by_date(pdfs, filter_datetime)
            
            result.append(FolderInfo(
                name=folder_name,
                pdf_count=len(filtered_pdfs),
                pdfs=filtered_pdfs
            ))
        
        # Sort folders alphabetically
        result.sort(key=lambda x: x.name)
        return result
        
    except Exception as e:
        logger.error(f"Error getting folders: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.get("/search", response_model=List[SearchResult])
async def search_pdfs_endpoint(
    q: str = Query(..., description="Search term"),
    target_datetime: Optional[str] = None
):
    """Search PDFs by filename and content"""
    try:
        if not q.strip():
            return []
        
        folders_data = scan_reports_directory()
        all_pdfs = []
        
        # Collect all PDFs from all folders
        for pdfs in folders_data.values():
            all_pdfs.extend(pdfs)
        
        # Parse target datetime if provided
        if target_datetime:
            try:
                filter_datetime = datetime.fromisoformat(target_datetime.replace('Z', '+00:00'))
                all_pdfs = filter_pdfs_by_date(all_pdfs, filter_datetime)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid datetime format")
        else:
            # Default to today 11:59:59 PM
            today = datetime.now().date()
            filter_datetime = datetime.combine(today, time(23, 59, 59))
            all_pdfs = filter_pdfs_by_date(all_pdfs, filter_datetime)
        
        # Perform search
        search_results = search_pdfs(all_pdfs, q)
        return search_results
        
    except Exception as e:
        logger.error(f"Error searching PDFs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.get("/pdf/{folder_name}/{filename}")
async def get_pdf(folder_name: str, filename: str):
    """Serve PDF file"""
    try:
        pdf_path = REPORTS_DIR / folder_name / filename
        
        if not pdf_path.exists() or not pdf_path.is_file():
            raise HTTPException(status_code=404, detail="PDF not found")
        
        if pdf_path.suffix.lower() != '.pdf':
            raise HTTPException(status_code=400, detail="Not a PDF file")
        
        return FileResponse(
            path=str(pdf_path),
            media_type='application/pdf',
            filename=filename
        )
        
    except Exception as e:
        logger.error(f"Error serving PDF {folder_name}/{filename}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.get("/pdf-info/{folder_name}/{filename}", response_model=PDFInfo)
async def get_pdf_info(folder_name: str, filename: str):
    """Get detailed PDF information"""
    try:
        pdf_path = REPORTS_DIR / folder_name / filename
        
        if not pdf_path.exists() or not pdf_path.is_file():
            raise HTTPException(status_code=404, detail="PDF not found")
        
        pdf_data = extract_pdf_metadata_and_text(pdf_path)
        if not pdf_data:
            raise HTTPException(status_code=500, detail="Could not process PDF")
        
        return PDFInfo(**pdf_data)
        
    except Exception as e:
        logger.error(f"Error getting PDF info {folder_name}/{filename}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()