import { useState } from 'react'
import { apiService } from './services/api'
import MediaInput from './components/MediaInput'
import TranscriptionView from './components/TranscriptionView'
import AnalysisView from './components/AnalysisView'
import StatusOverlay from './components/StatusOverlay'

function App() {
  const [status, setStatus] = useState('')
  const [progress, setProgress] = useState(0)
  const [loading, setLoading] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [summary, setSummary] = useState('')
  const [activeView, setActiveView] = useState('input') // input, transcript, analysis
  const [analysisType, setAnalysisType] = useState('')

  const handleUpload = async (file) => {
    if (!file) return
    setLoading(true)
    setStatus('Uploading recording...')
    
    try {
      const res = await apiService.uploadFile(file)
      setStatus('Standardizing audio format...')
      await handleTranscribe(res.file_path)
    } catch (err) {
      setStatus(`Upload failed: ${err.message}`)
      setLoading(false)
    }
  }

  const handleYouTube = async (url) => {
    if (!url) return
    setLoading(true)
    setStatus('Connecting to YouTube...')
    setProgress(0)

    const cleanup = apiService.youtubeTranscribeStream(
      url,
      (data) => {
        if (data.type === 'status') {
          setStatus(data.message)
          if (data.progress !== undefined) setProgress(data.progress)
        } else if (data.type === 'progress') {
          setProgress(data.progress)
        } else if (data.type === 'error') {
          setStatus(`YouTube Error: ${data.message}`)
          setLoading(false)
          setProgress(0)
        } else if (data.type === 'complete') {
          setTranscript(data.text)
          setStatus('Transcription successful.')
          setLoading(false)
          setProgress(0)
          setActiveView('transcript')
        }
      },
      (err) => {
        setStatus(`Error: ${err.message}`)
        setLoading(false)
        setProgress(0)
      }
    )

    return cleanup
  }

  const handleTranscribe = async (filePath) => {
    setStatus('Transcribing with AI...')
    try {
      const res = await apiService.transcribeAudio(filePath)
      setTranscript(res.text)
      setStatus('Ready to analyze.')
      setLoading(false)
      setActiveView('transcript')
    } catch (err) {
      setStatus(`Transcription Error: ${err.message}`)
      setLoading(false)
    }
  }

  const handleGenerate = async (type) => {
    if (!transcript) return
    setLoading(true)
    setStatus(`Generating ${type === 'meeting_notes' ? 'Meeting Notes' : 'Summary'}...`)
    setAnalysisType(type)
    
    try {
      const res = await apiService.generateContent(transcript, type)
      setSummary(res.content)
      setActiveView('analysis')
      setStatus('Analysis complete.')
      setLoading(false)
    } catch (err) {
      setStatus(`Generation Error: ${err.message}`)
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
        {activeView === 'input' && (
          <MediaInput 
            onUpload={handleUpload} 
            onYouTube={handleYouTube} 
            loading={loading} 
          />
        )}

        {activeView === 'transcript' && (
          <TranscriptionView 
            transcript={transcript} 
            onGenerate={handleGenerate} 
            loading={loading} 
          />
        )}

        {activeView === 'analysis' && (
          <AnalysisView 
            content={summary} 
            type={analysisType} 
            onBack={() => setActiveView('transcript')} 
          />
        )}

        {activeView !== 'input' && (
          <div className="mt-12 flex justify-center">
            <button 
              onClick={() => {
                setActiveView('input')
                setTranscript('')
                setSummary('')
              }}
              className="px-8 py-3 bg-white border border-gray-200 rounded-2xl font-bold text-gray-600 hover:bg-gray-50 transition-all shadow-sm"
            >
              Start New Project
            </button>
          </div>
        )}
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
