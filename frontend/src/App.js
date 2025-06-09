import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const PDFViewer = ({ pdfUrl, filename }) => {
  if (!pdfUrl) {
    return (
      <div className="flex items-center justify-center h-full bg-gray-50 rounded-lg">
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-4 text-gray-400">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
            </svg>
          </div>
          <p className="text-gray-500">Select a PDF to view</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full rounded-lg overflow-hidden border">
      <div className="bg-gray-100 px-4 py-2 border-b">
        <p className="text-sm font-medium text-gray-700">{filename}</p>
      </div>
      <iframe
        src={pdfUrl}
        className="w-full h-[calc(100%-40px)]"
        title={filename}
      />
    </div>
  );
};

const SearchResults = ({ results, onSelectPdf }) => {
  if (results.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No search results found</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-800">
        Search Results ({results.length})
      </h3>
      {results.map((result, index) => (
        <div
          key={index}
          className="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
          onClick={() => onSelectPdf(result.pdf)}
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h4 className="font-medium text-blue-600 hover:text-blue-800">
                {result.pdf.filename}
              </h4>
              <p className="text-sm text-gray-500 mb-2">
                {result.pdf.folder} • {new Date(result.pdf.modified_date).toLocaleDateString()}
              </p>
              <div className="space-y-1">
                {result.matches.slice(0, 2).map((match, matchIndex) => (
                  <p key={matchIndex} className="text-sm text-gray-700">
                    <span className="font-medium">
                      {match.split(':')[0]}:
                    </span>
                    {match.split(':').slice(1).join(':')}
                  </p>
                ))}
                {result.matches.length > 2 && (
                  <p className="text-sm text-gray-500">
                    +{result.matches.length - 2} more matches
                  </p>
                )}
              </div>
            </div>
            <span className="ml-4 text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
              {result.match_count} matches
            </span>
          </div>
        </div>
      ))}
    </div>
  );
};

const App = () => {
  const [folders, setFolders] = useState([]);
  const [selectedFolder, setSelectedFolder] = useState(null);
  const [selectedPdf, setSelectedPdf] = useState(null);
  const [targetDateTime, setTargetDateTime] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize target datetime to today 11:59:59 PM
  useEffect(() => {
    const today = new Date();
    today.setHours(23, 59, 59, 999);
    setTargetDateTime(today.toISOString().slice(0, 16));
  }, []);

  // Load folders
  const loadFolders = async () => {
    try {
      setLoading(true);
      setError(null);
      const params = targetDateTime ? { target_datetime: new Date(targetDateTime).toISOString() } : {};
      const response = await axios.get(`${API}/folders`, { params });
      setFolders(response.data);
      
      // Auto-select first folder if none selected
      if (response.data.length > 0 && !selectedFolder) {
        setSelectedFolder(response.data[0]);
      }
    } catch (err) {
      setError('Failed to load folders');
      console.error('Error loading folders:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFolders();
  }, [targetDateTime]);

  // Handle search
  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      setSearchResults([]);
      setIsSearching(false);
      return;
    }

    try {
      setIsSearching(true);
      const params = {
        q: searchTerm,
        ...(targetDateTime ? { target_datetime: new Date(targetDateTime).toISOString() } : {})
      };
      const response = await axios.get(`${API}/search`, { params });
      setSearchResults(response.data);
    } catch (err) {
      console.error('Error searching:', err);
      setSearchResults([]);
    }
  };

  // Handle search input change with debounce
  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchTerm.trim()) {
        handleSearch();
      } else {
        setSearchResults([]);
        setIsSearching(false);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [searchTerm, targetDateTime]);

  const handleSelectPdf = (pdf) => {
    const pdfUrl = `${API}/pdf/${pdf.folder}/${pdf.filename}`;
    setSelectedPdf({ ...pdf, url: pdfUrl });
    setSearchTerm(''); // Clear search when selecting a PDF
    setSearchResults([]);
    setIsSearching(false);
  };

  const handleFolderSelect = (folder) => {
    setSelectedFolder(folder);
    setSelectedPdf(null);
    setSearchTerm('');
    setSearchResults([]);
    setIsSearching(false);
  };

  const handleDateTimeChange = (e) => {
    setTargetDateTime(e.target.value);
    setSelectedPdf(null); // Clear selected PDF when date changes
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading reports...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={loadFolders}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <h1 className="text-xl font-semibold text-gray-900">
              PDF Reports Manager
            </h1>
            <div className="flex items-center space-x-4">
              <label className="text-sm font-medium text-gray-700">
                Target Date & Time:
              </label>
              <input
                type="datetime-local"
                value={targetDateTime}
                onChange={handleDateTimeChange}
                className="px-3 py-1 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex gap-6 h-[calc(100vh-140px)]">
          {/* Sidebar */}
          <div className="w-80 bg-white rounded-lg shadow-sm border p-4">
            {/* Search */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Search PDFs
              </label>
              <input
                type="text"
                placeholder="Search by filename or content..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* Show search results or folders */}
            <div className="flex-1 overflow-y-auto">
              {isSearching || searchResults.length > 0 ? (
                <SearchResults
                  results={searchResults}
                  onSelectPdf={handleSelectPdf}
                />
              ) : (
                <>
                  <h2 className="text-lg font-semibold text-gray-800 mb-4">
                    Folders
                  </h2>
                  <div className="space-y-2">
                    {folders.map((folder) => (
                      <button
                        key={folder.name}
                        onClick={() => handleFolderSelect(folder)}
                        className={`w-full text-left p-3 rounded-lg transition-colors ${
                          selectedFolder?.name === folder.name
                            ? 'bg-blue-100 text-blue-800 border border-blue-200'
                            : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
                        }`}
                      >
                        <div className="font-medium">{folder.name.replace('_', ' ')}</div>
                        <div className="text-sm text-gray-500">
                          {folder.pdf_count} PDFs
                        </div>
                      </button>
                    ))}
                  </div>

                  {/* PDFs in selected folder */}
                  {selectedFolder && selectedFolder.pdfs.length > 0 && (
                    <div className="mt-6">
                      <h3 className="text-md font-semibold text-gray-800 mb-3">
                        PDFs in {selectedFolder.name.replace('_', ' ')}
                      </h3>
                      <div className="space-y-2">
                        {selectedFolder.pdfs.map((pdf) => (
                          <button
                            key={pdf.filename}
                            onClick={() => handleSelectPdf(pdf)}
                            className={`w-full text-left p-2 rounded text-sm transition-colors ${
                              selectedPdf?.filename === pdf.filename
                                ? 'bg-green-100 text-green-800 border border-green-200'
                                : 'bg-white hover:bg-gray-50 text-gray-700 border'
                            }`}
                          >
                            <div className="font-medium truncate">{pdf.filename}</div>
                            <div className="text-xs text-gray-500">
                              {new Date(pdf.modified_date).toLocaleDateString()}
                            </div>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1 bg-white rounded-lg shadow-sm border">
            <PDFViewer
              pdfUrl={selectedPdf?.url}
              filename={selectedPdf?.filename}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;