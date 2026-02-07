import { useState } from 'react'
import axios from 'axios'

function App() {
  const [file, setFile] = useState(null)
  const [url, setUrl] = useState('')
  const [status, setStatus] = useState('')
  const [transcript, setTranscript] = useState('')
  const [summary, setSummary] = useState('')
  const [activeTab, setActiveTab] = useState('transcript')
  const [loading, setLoading] = useState(false)

  const handleFileChange = (e) => {
    if (e.target.files) {
      setFile(e.target.files[0])
    }
  }

  const handleUpload = async () => {
    if (!file) return
    setLoading(true)
    setStatus('Uploading...')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await axios.post('http://localhost:8000/api/upload', formData)
      setStatus(`Uploaded: ${res.data.original_filename}`)
      // Auto-trigger transcribe (in a real app, maybe separate step)
      await handleTranscribe(res.data.file_path)
    } catch (err) {
      setStatus(`Error: ${err.message}`)
      setLoading(false)
    }
  }

  const handleDownload = async () => {
    if (!url) return
    setLoading(true)
    setStatus('Downloading from YouTube...')

    try {
      const res = await axios.post('http://localhost:8000/api/download', { url })
      setStatus('Download complete. Transcribing...')
      await handleTranscribe(res.data.file_path)
    } catch (err) {
      setStatus(`Error: ${err.message}`)
      setLoading(false)
    }
  }

  const handleTranscribe = async (filePath) => {
    setStatus('Transcribing...')
    try {
      const res = await axios.post('http://localhost:8000/api/transcribe', {
        file_path: filePath,
        language: 'en' // Default to English for now, should add selector
      })
      setTranscript(res.data.text)
      setStatus('Transcription complete.')
      setLoading(false)
    } catch (err) {
      setStatus(`Transcription Error: ${err.message}`)
      setLoading(false)
    }
  }

  const handleGenerate = async (type) => {
    if (!transcript) return
    setLoading(true)
    setStatus(`Generating ${type}...`)
    try {
      const res = await axios.post('http://localhost:8000/api/generate', {
        transcript,
        template_type: type
      })
      setSummary(res.data.content)
      setActiveTab('summary')
      setStatus('Generation complete.')
      setLoading(false)
    } catch (err) {
      setStatus(`Generation Error: ${err.message}`)
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold mb-6 text-indigo-600">MeetingMind Web</h1>

        {/* Input Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="p-4 border rounded-lg bg-gray-50">
            <h2 className="text-lg font-semibold mb-2">Upload File</h2>
            <input
              type="file"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
            />
            <button
              onClick={handleUpload}
              disabled={!file || loading}
              className="mt-4 w-full bg-indigo-600 text-white py-2 px-4 rounded hover:bg-indigo-700 disabled:opacity-50"
            >
              Upload & Process
            </button>
          </div>

          <div className="p-4 border rounded-lg bg-gray-50">
            <h2 className="text-lg font-semibold mb-2">YouTube URL</h2>
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://youtube.com/..."
              className="w-full p-2 border rounded mb-4"
            />
            <button
              onClick={handleDownload}
              disabled={!url || loading}
              className="mt-0 w-full bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700 disabled:opacity-50"
            >
              Download & Process
            </button>
          </div>
        </div>

        {/* Status Bar */}
        {status && (
          <div className="bg-blue-50 text-blue-700 p-3 rounded mb-6 text-center animate-pulse">
            {status}
          </div>
        )}

        {/* Content Area */}
        {transcript && (
          <div>
            <div className="flex border-b mb-4">
              <button
                className={`py-2 px-4 ${activeTab === 'transcript' ? 'border-b-2 border-indigo-600 text-indigo-600 font-bold' : 'text-gray-500'}`}
                onClick={() => setActiveTab('transcript')}
              >
                Transcript
              </button>
              <button
                className={`py-2 px-4 ${activeTab === 'summary' ? 'border-b-2 border-indigo-600 text-indigo-600 font-bold' : 'text-gray-500'}`}
                onClick={() => setActiveTab('summary')}
              >
                Summary / Notes
              </button>
            </div>

            <div className="bg-gray-50 p-6 rounded-lg min-h-[300px] whitespace-pre-wrap">
              {activeTab === 'transcript' ? (
                <div>
                  <div className="flex justify-end space-x-2 mb-4">
                    <button onClick={() => handleGenerate('meeting_notes')} className="text-sm bg-green-600 text-white px-3 py-1 rounded">Generate Notes</button>
                    <button onClick={() => handleGenerate('summary')} className="text-sm bg-blue-600 text-white px-3 py-1 rounded">Generate Summary</button>
                  </div>
                  <p className="text-gray-800 leading-relaxed">{transcript}</p>
                </div>
              ) : (
                <div className="prose max-w-none">
                  <h3 className="text-xl font-bold mb-4">Generated Content</h3>
                  <div dangerouslySetInnerHTML={{ __html: summary.replace(/\n/g, '<br/>') }} />
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
