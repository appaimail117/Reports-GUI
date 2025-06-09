#!/usr/bin/env python3
"""
Script to create sample PDFs with different content and dates for testing
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import random

def create_pdf_with_content(filename, title, content, creation_date):
    """Create a PDF with specific content and modify its creation date"""
    
    # Create the PDF
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
    )
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))
    
    # Content
    for paragraph in content:
        story.append(Paragraph(paragraph, styles['Normal']))
        story.append(Spacer(1, 12))
    
    # Add creation date info
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"<i>Document created: {creation_date.strftime('%Y-%m-%d %H:%M:%S')}</i>", styles['Italic']))
    
    doc.build(story)
    
    # Modify file timestamp to simulate different creation dates
    timestamp = creation_date.timestamp()
    os.utime(filename, (timestamp, timestamp))

def main():
    reports_dir = Path("/app/reports")
    
    # Create folder structure
    folders = [
        "financial_reports",
        "marketing_analytics", 
        "project_updates",
        "technical_docs",
        "hr_documents"
    ]
    
    for folder in folders:
        (reports_dir / folder).mkdir(parents=True, exist_ok=True)
    
    # Sample PDFs with different content and dates
    pdf_data = [
        # Financial Reports
        {
            "folder": "financial_reports",
            "filename": "Q1_2024_Revenue_Report.pdf",
            "title": "Q1 2024 Revenue Analysis",
            "content": [
                "This quarterly revenue report provides comprehensive analysis of our financial performance.",
                "Total revenue for Q1 2024 reached $2.5 million, representing a 15% increase from Q4 2023.",
                "Key growth drivers include expansion in the enterprise segment and successful product launches.",
                "Operating expenses were controlled at $1.8 million, maintaining healthy profit margins.",
                "Cash flow remained positive throughout the quarter with strong collection rates."
            ],
            "days_ago": 45
        },
        {
            "folder": "financial_reports", 
            "filename": "Budget_Forecast_2024.pdf",
            "title": "Annual Budget Forecast 2024",
            "content": [
                "Annual budget planning document outlining financial projections for 2024.",
                "Projected revenue growth of 25% based on market expansion plans.",
                "Investment allocation: 40% R&D, 30% Sales & Marketing, 20% Operations, 10% Infrastructure.",
                "Risk factors include market volatility and supply chain disruptions.",
                "Contingency planning includes scenario analysis for various market conditions."
            ],
            "days_ago": 120
        },
        
        # Marketing Analytics
        {
            "folder": "marketing_analytics",
            "filename": "Campaign_Performance_Jan2024.pdf", 
            "title": "January 2024 Marketing Campaign Results",
            "content": [
                "Monthly marketing campaign performance analysis and optimization recommendations.",
                "Digital advertising ROI improved to 3.2x with targeted audience segmentation.",
                "Social media engagement increased by 45% following content strategy revision.",
                "Email marketing conversion rates reached 8.5%, exceeding industry benchmarks.",
                "Lead generation pipeline shows strong correlation with brand awareness metrics."
            ],
            "days_ago": 60
        },
        {
            "folder": "marketing_analytics",
            "filename": "Customer_Segmentation_Study.pdf",
            "title": "Customer Segmentation Analysis",
            "content": [
                "Comprehensive customer segmentation study using behavioral and demographic data.",
                "Identified five distinct customer personas with varying purchase patterns.",
                "Enterprise customers show highest lifetime value but longer sales cycles.", 
                "SMB segment demonstrates quick adoption but requires different support strategies.",
                "Personalization opportunities exist across all segments for improved engagement."
            ],
            "days_ago": 30
        },
        
        # Project Updates
        {
            "folder": "project_updates",
            "filename": "Project_Alpha_Status.pdf",
            "title": "Project Alpha - Weekly Status Update",
            "content": [
                "Weekly project status update for Project Alpha development initiative.",
                "Development milestone achieved: core functionality implementation completed.",
                "Testing phase initiated with automated test coverage at 85%.",
                "Integration challenges identified with legacy systems requiring additional work.",
                "Timeline remains on track for Q2 2024 launch with minor scope adjustments."
            ],
            "days_ago": 7
        },
        {
            "folder": "project_updates",
            "filename": "Infrastructure_Upgrade_Plan.pdf", 
            "title": "Infrastructure Modernization Plan",
            "content": [
                "Strategic plan for modernizing IT infrastructure and cloud migration.",
                "Phase 1: Database migration to cloud-native solutions by Q3 2024.",
                "Phase 2: Application containerization and microservices architecture.",
                "Security enhancements include zero-trust network implementation.",
                "Cost analysis shows 30% reduction in operational expenses post-migration."
            ],
            "days_ago": 15
        },
        
        # Technical Documentation
        {
            "folder": "technical_docs",
            "filename": "API_Documentation_v2.pdf",
            "title": "API Documentation Version 2.0",
            "content": [
                "Technical documentation for REST API version 2.0 implementation.",
                "Authentication methods include OAuth 2.0 and API key management.",
                "Rate limiting implemented to ensure system stability and fair usage.",
                "Response formats standardized with comprehensive error handling.",
                "SDK available in Python, JavaScript, and Java for developer integration."
            ],
            "days_ago": 25
        },
        {
            "folder": "technical_docs",
            "filename": "Security_Audit_Report.pdf",
            "title": "Annual Security Audit Report",
            "content": [
                "Comprehensive security audit covering infrastructure, applications, and processes.",
                "Vulnerability assessment identified minimal critical issues, all addressed.",
                "Penetration testing results show robust defense mechanisms in place.",
                "Compliance verification for SOC 2 Type II and ISO 27001 standards.",
                "Recommendations include enhanced monitoring and incident response procedures."
            ],
            "days_ago": 90
        },
        
        # HR Documents
        {
            "folder": "hr_documents",
            "filename": "Employee_Handbook_2024.pdf",
            "title": "Employee Handbook 2024 Edition", 
            "content": [
                "Updated employee handbook covering policies, procedures, and benefits.",
                "Remote work guidelines and hybrid collaboration best practices.",
                "Professional development opportunities including training and certification programs.",
                "Health and wellness benefits expanded to include mental health support.",
                "Code of conduct and ethics guidelines for all team members."
            ],
            "days_ago": 100
        },
        {
            "folder": "hr_documents",
            "filename": "Recruitment_Strategy.pdf",
            "title": "2024 Talent Acquisition Strategy",
            "content": [
                "Strategic approach to talent acquisition and retention for 2024.",
                "Focus on diversity, equity, and inclusion in hiring practices.",
                "Employer branding initiatives to attract top-tier candidates.",
                "Compensation benchmarking against industry standards completed.",
                "Onboarding process optimization for improved new hire experience."
            ],
            "days_ago": 50
        }
    ]
    
    # Create PDFs
    for pdf_info in pdf_data:
        folder_path = reports_dir / pdf_info["folder"]
        file_path = folder_path / pdf_info["filename"]
        
        # Calculate creation date
        creation_date = datetime.now() - timedelta(days=pdf_info["days_ago"])
        
        # Add some random hours/minutes to make dates more realistic
        creation_date = creation_date.replace(
            hour=random.randint(8, 18),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )
        
        print(f"Creating: {file_path}")
        create_pdf_with_content(
            str(file_path),
            pdf_info["title"], 
            pdf_info["content"],
            creation_date
        )
    
    print(f"\nSample PDFs created successfully!")
    print(f"Total folders: {len(folders)}")
    print(f"Total PDFs: {len(pdf_data)}")
    
    # List created structure
    print("\nCreated structure:")
    for folder in folders:
        folder_path = reports_dir / folder
        pdfs = list(folder_path.glob("*.pdf"))
        print(f"  {folder}/")
        for pdf in pdfs:
            stat = pdf.stat()
            mod_time = datetime.fromtimestamp(stat.st_mtime)
            print(f"    - {pdf.name} (Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')})")

if __name__ == "__main__":
    main()