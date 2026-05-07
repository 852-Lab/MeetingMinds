import React from 'react';

const features = [
  {
    title: 'Real-time Session',
    description: 'Automatic screenshot capture during meetings with synchronized voice recording and live transcription.',
    icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
      </svg>
    ),
    color: 'indigo'
  },
  {
    title: 'Advanced Video Support',
    description: 'Full video processing in addition to audio, extracting visual context for more comprehensive meeting notes.',
    icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
      </svg>
    ),
    color: 'purple'
  },
  {
    title: 'Native Clients',
    description: 'Experience MeetingMinds natively on iOS and MacOS. Seamless synchronization and optimized performance for your favorite platforms.',
    icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2zM9 17h6M9 13h6" />
      </svg>
    ),
    color: 'pink'
  }
];

const UpcomingFeatures = () => {
  return (
    <section className="mt-24 mb-12">
      <div className="flex items-center justify-between mb-10">
        <div>
          <h2 className="text-3xl font-black text-gray-900 tracking-tight">Upcoming Features</h2>
          <p className="text-gray-500 font-medium mt-1">Our roadmap to the future of meeting intelligence.</p>
        </div>
        <div className="hidden md:block">
          <span className="px-4 py-2 bg-indigo-50 text-indigo-600 rounded-full text-sm font-bold border border-indigo-100 uppercase tracking-widest">
            Roadmap 2026
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {features.map((feature, index) => (
          <div 
            key={index}
            className="group relative bg-white border border-gray-100 p-8 rounded-[2rem] shadow-sm hover:shadow-xl hover:border-indigo-100 transition-all duration-500 overflow-hidden"
          >
            {/* Background Gradient Glow */}
            <div className={`absolute -right-10 -top-10 w-32 h-32 bg-${feature.color}-500/5 blur-3xl group-hover:bg-${feature.color}-500/10 transition-colors duration-500 rounded-full`}></div>
            
            <div className={`inline-flex p-4 rounded-2xl mb-6 bg-${feature.color}-50 text-${feature.color}-600 group-hover:scale-110 transition-transform duration-500 ring-1 ring-${feature.color}-100`}>
              {feature.icon}
            </div>
            
            <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-indigo-600 transition-colors duration-300">
              {feature.title}
            </h3>
            
            <p className="text-gray-500 leading-relaxed text-sm font-medium">
              {feature.description}
            </p>

            <div className="mt-8 pt-6 border-t border-gray-50 flex items-center text-xs font-bold text-gray-400 uppercase tracking-widest group-hover:text-indigo-500 transition-colors duration-300">
              <span>Coming Soon</span>
              <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default UpcomingFeatures;
