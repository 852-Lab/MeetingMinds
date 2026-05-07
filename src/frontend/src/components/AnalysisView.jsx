import React from 'react';

const AnalysisView = ({ content, type, onBack }) => {
  if (!content) return null;

  return (
    <div className="animate-in fade-in slide-in-from-right-4 duration-700">
      <div className="flex items-center justify-between mb-8">
        <div>
          <button 
            onClick={onBack}
            className="group flex items-center text-sm font-bold text-indigo-600 mb-2 hover:text-indigo-800 transition-colors"
          >
            <svg className="w-4 h-4 mr-1 transform group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back to Transcript
          </button>
          <h3 className="text-3xl font-black text-gray-900 tracking-tight">
            {type === 'meeting_notes' ? 'Meeting Insights' : 'Executive Summary'}
          </h3>
        </div>
        
        <button 
          onClick={() => window.print()}
          className="p-3 bg-white border border-gray-200 rounded-2xl text-gray-600 hover:bg-gray-50 transition-all shadow-sm"
          title="Print or Export PDF"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
          </svg>
        </button>
      </div>

      <div className="bg-white/70 backdrop-blur-xl border border-white/60 p-10 rounded-[2.5rem] shadow-2xl">
        <div className="prose prose-indigo max-w-none prose-headings:font-black prose-p:text-gray-700 prose-p:leading-relaxed text-lg">
          <div dangerouslySetInnerHTML={{ __html: content.replace(/\n/g, '<br/>') }} />
        </div>
      </div>
    </div>
  );
};

export default AnalysisView;
