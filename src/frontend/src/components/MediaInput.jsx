import React, { useState } from 'react';

const MediaInput = ({ onUpload, onYouTube, loading, sonaReady }) => {
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
        
        <div className="relative">
          <input
            type="file"
            id="file-upload"
            onChange={handleFileChange}
            className="hidden"
            accept=".mp3,.mp4,.wav,.m4a,.aac"
          />
          <label
            htmlFor="file-upload"
            className="flex items-center justify-between w-full p-4 bg-white/50 border-2 border-dashed border-gray-200 rounded-2xl cursor-pointer hover:border-indigo-400 hover:bg-indigo-50/30 transition-all group/upload"
          >
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-indigo-100 rounded-xl text-indigo-600 group-hover/upload:scale-110 transition-transform">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                </svg>
              </div>
              <div>
                <p className="text-sm font-bold text-gray-700">
                  {file ? file.name : 'Select Audio/Video'}
                </p>
                <p className="text-xs text-gray-400 font-medium">MP3, MP4, WAV, M4A supported</p>
              </div>
            </div>
            <span className="text-xs font-bold text-indigo-600 uppercase tracking-widest">Browse</span>
          </label>
        </div>
        
        <button
          onClick={() => onUpload(file)}
          disabled={!file || loading || !sonaReady}
          className="mt-6 w-full bg-indigo-600 text-white py-3.5 rounded-2xl font-bold hover:bg-indigo-700 disabled:opacity-50 transition-all shadow-lg shadow-indigo-100 active:scale-95"
        >
          {sonaReady ? 'Start Processing' : 'Waiting for Engine...'}
        </button>
        <p className="mt-4 text-center text-xs text-gray-400 font-medium">
          Est. processing: ~1-2m per 10m of audio
        </p>
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
          disabled={!url || loading || !sonaReady}
          className="w-full bg-red-600 text-white py-3.5 rounded-2xl font-bold hover:bg-red-700 disabled:opacity-50 transition-all shadow-lg shadow-red-200 active:scale-95"
        >
          {sonaReady ? 'Extract Transcript' : 'Waiting for Engine...'}
        </button>
        <p className="mt-4 text-center text-xs text-gray-400 font-medium">
          Est. processing: ~1-2m per 10m of audio
        </p>
      </div>
    </div>
  );
};

export default MediaInput;
