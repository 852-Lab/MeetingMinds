import { useState, useEffect } from 'react'
import { apiService } from './services/api'
import MediaInput from './components/MediaInput'
import StatusOverlay from './components/StatusOverlay'
import JobsList from './components/JobsList'
import UpcomingFeatures from './components/UpcomingFeatures'
import SettingsPanel from './components/SettingsPanel'

function App() {
  const [status, setStatus] = useState('')
  const [progress, setProgress] = useState(0)
  const [loading, setLoading] = useState(false)
  const [sonaReady, setSonaReady] = useState(true)
  const [openaiKeyConfigured, setOpenaiKeyConfigured] = useState(false)

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const res = await apiService.getSonaStatus()
        setSonaReady(res.ready)
      } catch (err) {
        setSonaReady(false)
      }
    }

    checkStatus()
    const interval = setInterval(checkStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleUpload = async (file) => {
    if (!file) return
    setLoading(true)
    setStatus('Uploading recording...')
    
    try {
      await apiService.uploadFile(file)
      setStatus('Success! Your recording is in the queue for processing.')
      setTimeout(() => {
        setLoading(false)
        setStatus('')
      }, 3000)
    } catch (err) {
      setStatus(`Upload failed: ${err.message}`)
      setLoading(false)
    }
  }

  const handleYouTube = async (url) => {
    if (!url) return
    setLoading(true)
    setStatus('Queueing YouTube video...')
    
    try {
      await apiService.youtubeTranscribe(url)
      setStatus('Success! Video URL is in the queue for processing.')
      setTimeout(() => {
        setLoading(false)
        setStatus('')
      }, 3000)
    } catch (err) {
      setStatus(`Error: ${err.message}`)
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#F8FAFC] selection:bg-indigo-100 selection:text-indigo-900">
      <StatusOverlay status={status} progress={progress} loading={loading} />

      {/* Hero Header */}
      <header className="pt-20 pb-16 px-6">
        <div className="max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center space-x-2 bg-white px-4 py-2 rounded-2xl shadow-sm border border-gray-100 mb-6">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-bold text-gray-500 uppercase tracking-widest">AI Core Active</span>
          </div>
          <h1 className="text-6xl font-black text-gray-900 mb-6 tracking-tight">
            Meeting<span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">Minds</span>
          </h1>
          <p className="text-xl text-gray-500 max-w-2xl mx-auto leading-relaxed">
            Transform your voice recordings and videos into actionable insights with state-of-the-art AI.
          </p>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 pb-24">
        {!sonaReady && !openaiKeyConfigured && (
          <div className="mb-8 p-4 bg-amber-50 border border-amber-200 rounded-2xl flex items-center space-x-4 animate-pulse">
            <div className="p-2 bg-amber-100 rounded-xl text-amber-600">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p className="text-amber-800 font-bold">Transcription Engine Initializing</p>
              <p className="text-amber-700 text-sm font-medium">
                Downloading AI models (~1.5GB). This may take 2-5 minutes on the first run.
                Once ready, transcription takes about 1-2 minutes for every 10 minutes of audio.
              </p>
            </div>
          </div>
        )}

        <div className="space-y-12">
          <section className="animate-fade-in">
            <SettingsPanel onKeyStatusChange={setOpenaiKeyConfigured} />
          </section>

          <section className="animate-fade-in">
            <MediaInput
              onUpload={handleUpload}
              onYouTube={handleYouTube}
              loading={loading}
              sonaReady={sonaReady || openaiKeyConfigured}
            />
          </section>

          <section className="animate-fade-in" style={{ animationDelay: '0.1s' }}>
            <JobsList />
          </section>

          <section className="animate-fade-in" style={{ animationDelay: '0.2s' }}>
            <UpcomingFeatures />
          </section>
        </div>
      </main>

      <footer className="py-12 border-t border-gray-100 bg-white">
        <div className="max-w-5xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
          <p className="text-gray-400 font-medium">© 2026 MeetingMinds AI. All rights reserved.</p>
          <div className="flex space-x-8">
            <a href="#" className="text-gray-400 hover:text-indigo-600 transition-colors font-bold uppercase tracking-widest text-xs">Privacy</a>
            <a href="#" className="text-gray-400 hover:text-indigo-600 transition-colors font-bold uppercase tracking-widest text-xs">Terms</a>
            <a href="#" className="text-gray-400 hover:text-indigo-600 transition-colors font-bold uppercase tracking-widest text-xs">Support</a>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
