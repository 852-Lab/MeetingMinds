import { useState, useEffect } from 'react'
import { apiService } from '../services/api'

function JobsList() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchJobs = async () => {
    try {
      const data = await apiService.getJobs()
      setJobs(data)
    } catch (err) {
      console.error('Failed to fetch jobs:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchJobs()
    const interval = setInterval(fetchJobs, 3000)
    return () => clearInterval(interval)
  }, [])

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'bg-amber-100 text-amber-700'
      case 'processing': return 'bg-blue-100 text-blue-700'
      case 'completed': return 'bg-green-100 text-green-700'
      case 'failed': return 'bg-red-100 text-red-700'
      default: return 'bg-gray-100 text-gray-700'
    }
  }

  return (
    <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="px-8 py-6 border-b border-gray-50 flex items-center justify-between">
        <h2 className="text-2xl font-black text-gray-900">Active Queue</h2>
        <div className="px-4 py-1 bg-indigo-50 rounded-full">
          <span className="text-sm font-bold text-indigo-600 uppercase tracking-widest">
            {jobs.length} Job{jobs.length !== 1 ? 's' : ''}
          </span>
        </div>
      </div>

      <div className="divide-y divide-gray-50">
        {jobs.length === 0 ? (
          <div className="px-8 py-12 text-center">
            <p className="text-gray-400 font-medium italic">No jobs in queue. Start a new project above.</p>
          </div>
        ) : (
          jobs.map((job) => (
            <div key={job.id} className="px-8 py-6 hover:bg-gray-50/50 transition-colors">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-1">
                    <span className={`px-2.5 py-0.5 rounded-lg text-[10px] font-black uppercase tracking-wider ${getStatusColor(job.status)}`}>
                      {job.status}
                    </span>
                    <span className="text-xs font-bold text-gray-400 uppercase tracking-widest">
                      {new Date(job.created_at).toLocaleTimeString()}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-gray-800 truncate max-w-md">
                    {job.original_filename || job.input_path}
                  </h3>
                  <p className="text-sm text-gray-400 font-medium">
                    ID: {job.id.substring(0, 8)}... • Type: {job.type.replace('_', ' ')}
                  </p>
                </div>

                <div className="flex items-center space-x-3">
                  {job.status === 'completed' && (
                    <>
                      <a 
                        href={apiService.getTranscriptUrl(job.id)}
                        download
                        className="px-4 py-2 bg-white border border-gray-200 rounded-xl text-sm font-bold text-gray-600 hover:bg-gray-50 transition-all flex items-center space-x-2 shadow-sm"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <span>Transcript</span>
                      </a>
                      <a 
                        href={apiService.getSummaryUrl(job.id)}
                        download
                        className="px-4 py-2 bg-indigo-600 rounded-xl text-sm font-bold text-white hover:bg-indigo-700 transition-all flex items-center space-x-2 shadow-md shadow-indigo-100"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                        </svg>
                        <span>Summary</span>
                      </a>
                    </>
                  )}
                  {job.status === 'failed' && (
                    <div className="text-xs text-red-500 font-bold max-w-xs text-right">
                      {job.error_message || 'Unknown error occurred during processing.'}
                    </div>
                  )}
                  {job.status === 'processing' && (
                    <div className="flex items-center space-x-2 text-blue-600">
                      <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                      <span className="text-sm font-black uppercase tracking-widest">Processing</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default JobsList
