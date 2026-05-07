import React from 'react';

const StatusOverlay = ({ status, progress, loading }) => {
  if (!status && !loading) return null;

  return (
    <div className="fixed top-6 left-1/2 transform -translate-x-1/2 z-50 w-full max-w-md px-4">
      <div className={`
        bg-white/80 backdrop-blur-md border border-white/20 shadow-2xl rounded-2xl p-4
        transition-all duration-500 ease-in-out transform
        ${status ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0'}
      `}>
        <div className="flex items-center space-x-3">
          {loading && (
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0s' }}></div>
              <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
            </div>
          )}
          <p className="text-sm font-medium text-gray-700 truncate">{status}</p>
        </div>
        
        {loading && progress > 0 && (
          <div className="mt-3 w-full bg-gray-200/50 rounded-full h-1.5 overflow-hidden">
            <div
              className="bg-gradient-to-r from-indigo-500 to-purple-500 h-full rounded-full transition-all duration-300 ease-out shadow-[0_0_10px_rgba(99,102,241,0.5)]"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default StatusOverlay;
