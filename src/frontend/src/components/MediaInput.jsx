import React, { useState } from 'react';

const MediaInput = ({ onUpload, onYouTube, loading }) => {
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState('');

  const handleFileChange = (e) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
      {/* File Upload Card */}
      <div className="group bg-white/40 backdrop-blur-lg border border-white/40 p-8 rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
        <div className="flex items-center space-x-4 mb-6">
          <div className="p-3 bg-indigo-100 rounded-2xl text-indigo-600">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <h2 className="text-xl font-bold text-gray-800">Upload Recording</h2>
        </div>
        
        <label className="block w-full">
          <span className="sr-only">Choose file</span>
          <input
            type="file"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2.5 file:px-6 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-indigo-600 file:text-white hover:file:bg-indigo-700 transition-colors cursor-pointer"
          />
        </label>
        
        <button
          onClick={() => onUpload(file)}
          disabled={!file || loading}
          className="mt-6 w-full bg-white text-indigo-600 border-2 border-indigo-600 py-3 rounded-2xl font-bold hover:bg-indigo-50 disabled:opacity-50 disabled:hover:bg-white transition-all shadow-md active:scale-95"
        >
          Process File
        </button>
      </div>

      {/* YouTube Card */}
      <div className="group bg-white/40 backdrop-blur-lg border border-white/40 p-8 rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
        <div className="flex items-center space-x-4 mb-6">
          <div className="p-3 bg-red-100 rounded-2xl text-red-600">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold text-gray-800">YouTube Video</h2>
        </div>

        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Paste YouTube link here..."
          className="w-full p-3.5 bg-white/50 border border-gray-200 rounded-2xl mb-6 focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none transition-all placeholder:text-gray-400"
        />
        
        <button
          onClick={() => onYouTube(url)}
          disabled={!url || loading}
          className="w-full bg-red-600 text-white py-3.5 rounded-2xl font-bold hover:bg-red-700 disabled:opacity-50 transition-all shadow-lg shadow-red-200 active:scale-95"
        >
          Extract Transcript
        </button>
      </div>
    </div>
  );
};

export default MediaInput;
