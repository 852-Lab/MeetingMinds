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

  async getSonaStatus() {
    const response = await api.get('/sona-status');
    return response.data;
  },

  async getJobs() {
    const response = await api.get('/jobs/');
    return response.data;
  },

  async getJob(jobId) {
    const response = await api.get(`/jobs/${jobId}`);
    return response.data;
  },

  async youtubeTranscribe(url) {
    const response = await api.post('/youtube-transcribe', { url });
    return response.data;
  },

  getTranscriptUrl(jobId) {
    return `${API_BASE_URL}/jobs/${jobId}/transcript`;
  },

  getSummaryUrl(jobId) {
    return `${API_BASE_URL}/jobs/${jobId}/summary`;
  }
};
