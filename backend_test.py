import requests
import unittest
import json
from datetime import datetime, timedelta
import sys

# Get the backend URL from the frontend .env file
BACKEND_URL = "https://ece3a514-43ed-4d27-b14a-09494f219ac8.preview.emergentagent.com"
API_URL = f"{BACKEND_URL}/api"

class PDFReportsAPITest(unittest.TestCase):
    """Test suite for the PDF Reports Management API"""

    def test_01_root_endpoint(self):
        """Test the root API endpoint"""
        print("\n🔍 Testing root API endpoint...")
        response = requests.get(f"{API_URL}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "PDF Reports Management API")
        print("✅ Root API endpoint is working")

    def test_02_folders_endpoint(self):
        """Test the folders endpoint"""
        print("\n🔍 Testing folders endpoint...")
        response = requests.get(f"{API_URL}/folders")
        self.assertEqual(response.status_code, 200)
        folders = response.json()
        
        # Verify we have the expected folders
        folder_names = [folder["name"] for folder in folders]
        expected_folders = ["financial_reports", "hr_documents", "marketing_analytics", 
                           "project_updates", "technical_docs"]
        
        for folder in expected_folders:
            self.assertIn(folder, folder_names, f"Expected folder {folder} not found")
        
        # Verify folder structure
        for folder in folders:
            self.assertIn("name", folder)
            self.assertIn("pdf_count", folder)
            self.assertIn("pdfs", folder)
            self.assertIsInstance(folder["pdfs"], list)
            
            # Check PDF structure if there are any PDFs
            if folder["pdfs"]:
                pdf = folder["pdfs"][0]
                self.assertIn("filename", pdf)
                self.assertIn("filepath", pdf)
                self.assertIn("folder", pdf)
                self.assertIn("size", pdf)
                self.assertIn("created_date", pdf)
                self.assertIn("modified_date", pdf)
        
        print(f"✅ Folders endpoint returned {len(folders)} folders with correct structure")

    def test_03_date_filtering(self):
        """Test date filtering in folders endpoint"""
        print("\n🔍 Testing date filtering...")
        
        # Get all PDFs with default date (today)
        response_default = requests.get(f"{API_URL}/folders")
        folders_default = response_default.json()
        
        # Get PDFs with a past date (1 year ago)
        past_date = (datetime.now() - timedelta(days=365)).isoformat()
        response_past = requests.get(f"{API_URL}/folders", params={"target_datetime": past_date})
        folders_past = response_past.json()
        
        # The past date should return fewer or equal PDFs
        total_pdfs_default = sum(folder["pdf_count"] for folder in folders_default)
        total_pdfs_past = sum(folder["pdf_count"] for folder in folders_past)
        
        self.assertLessEqual(total_pdfs_past, total_pdfs_default)
        print(f"✅ Date filtering works: {total_pdfs_past} PDFs with past date vs {total_pdfs_default} with current date")

    def test_04_search_endpoint(self):
        """Test the search endpoint"""
        print("\n🔍 Testing search endpoint...")
        
        # Test search with a common term that should be in some PDFs
        search_term = "revenue"
        response = requests.get(f"{API_URL}/search", params={"q": search_term})
        self.assertEqual(response.status_code, 200)
        results = response.json()
        
        # Verify search results structure
        if results:
            result = results[0]
            self.assertIn("pdf", result)
            self.assertIn("matches", result)
            self.assertIn("match_count", result)
            
            # Check if the search term is in the matches
            found = False
            for match in result["matches"]:
                if search_term.lower() in match.lower():
                    found = True
                    break
            
            self.assertTrue(found, f"Search term '{search_term}' not found in matches")
            print(f"✅ Search endpoint found {len(results)} results for '{search_term}'")
        else:
            print(f"⚠️ No results found for search term '{search_term}', trying another term...")
            
            # Try another search term
            search_term = "marketing"
            response = requests.get(f"{API_URL}/search", params={"q": search_term})
            self.assertEqual(response.status_code, 200)
            results = response.json()
            
            if results:
                print(f"✅ Search endpoint found {len(results)} results for '{search_term}'")
            else:
                self.fail("Search endpoint returned no results for multiple search terms")

    def test_05_pdf_serving_endpoint(self):
        """Test the PDF serving endpoint"""
        print("\n🔍 Testing PDF serving endpoint...")
        
        # First get a list of folders and PDFs
        response = requests.get(f"{API_URL}/folders")
        folders = response.json()
        
        # Find a PDF to test
        pdf_found = False
        for folder in folders:
            if folder["pdfs"]:
                folder_name = folder["name"]
                pdf_filename = folder["pdfs"][0]["filename"]
                pdf_found = True
                break
        
        if not pdf_found:
            self.fail("No PDFs found to test the PDF serving endpoint")
        
        # Test the PDF serving endpoint
        pdf_url = f"{API_URL}/pdf/{folder_name}/{pdf_filename}"
        response = requests.get(pdf_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/pdf")
        
        # Check if the response contains PDF data (should start with %PDF)
        self.assertTrue(response.content.startswith(b"%PDF"), "Response is not a valid PDF")
        
        print(f"✅ PDF serving endpoint successfully returned {pdf_filename}")

    def test_06_pdf_info_endpoint(self):
        """Test the PDF info endpoint"""
        print("\n🔍 Testing PDF info endpoint...")
        
        # First get a list of folders and PDFs
        response = requests.get(f"{API_URL}/folders")
        folders = response.json()
        
        # Find a PDF to test
        pdf_found = False
        for folder in folders:
            if folder["pdfs"]:
                folder_name = folder["name"]
                pdf_filename = folder["pdfs"][0]["filename"]
                pdf_found = True
                break
        
        if not pdf_found:
            self.fail("No PDFs found to test the PDF info endpoint")
        
        # Test the PDF info endpoint
        info_url = f"{API_URL}/pdf-info/{folder_name}/{pdf_filename}"
        response = requests.get(info_url)
        
        self.assertEqual(response.status_code, 200)
        pdf_info = response.json()
        
        # Verify PDF info structure
        self.assertEqual(pdf_info["filename"], pdf_filename)
        self.assertEqual(pdf_info["folder"], folder_name)
        self.assertIn("size", pdf_info)
        self.assertIn("created_date", pdf_info)
        self.assertIn("modified_date", pdf_info)
        self.assertIn("text_content", pdf_info)
        
        print(f"✅ PDF info endpoint successfully returned metadata for {pdf_filename}")

def run_tests():
    """Run the test suite"""
    print("🚀 Starting PDF Reports API Tests")
    print(f"🌐 Testing API at: {API_URL}")
    
    # Create a test suite and run it
    suite = unittest.TestLoader().loadTestsFromTestCase(PDFReportsAPITest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    # Return the number of failures and errors
    return len(result.failures) + len(result.errors)

if __name__ == "__main__":
    sys.exit(run_tests())
