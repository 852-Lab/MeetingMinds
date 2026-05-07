import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const apiService = {
  async uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/upload', formData);
    return response.data;
  },

  async transcribeAudio(filePath, language = 'en') {
    const response = await api.post('/transcribe', {
      file_path: filePath,
      language,
    });
    return response.data;
  },

  async generateContent(transcript, templateType) {
    const response = await api.post('/generate', {
      transcript,
      template_type: templateType,
    });
    return response.data;
  },

  async downloadAudio(url) {
    const response = await api.post('/download', { url });
    return response.data;
  },

  // Streaming YouTube transcription
  youtubeTranscribeStream(url, onMessage, onError, onComplete) {
    const controller = new AbortController();
    
    fetch(`${API_BASE_URL}/youtube-transcribe`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
      signal: controller.signal,
    })
    .then(response => {
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return response.body.getReader();
    })
    .then(async (reader) => {
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop();

        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const data = JSON.parse(line);
            onMessage(data);
          } catch (e) {
            console.error('Error parsing stream chunk:', e, line);
          }
        }
      }
      onComplete && onComplete();
    })
    .catch(err => {
      if (err.name !== 'AbortError') {
        onError(err);
      }
    });

    return () => controller.abort();
  }
};
