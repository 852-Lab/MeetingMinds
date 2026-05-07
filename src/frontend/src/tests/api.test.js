import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';

// Mock axios BEFORE importing apiService
vi.mock('axios', () => {
  const mockAxios = {
    post: vi.fn(),
    create: vi.fn(function() { return this; }),
  };
  return { default: mockAxios };
});

import { apiService } from '../services/api';

describe('apiService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('uploadFile should send a POST request with FormData', async () => {
    axios.post.mockResolvedValue({ data: { message: 'Uploaded' } });
    
    const file = new File(['content'], 'test.mp3');
    const result = await apiService.uploadFile(file);
    
    expect(axios.post).toHaveBeenCalledWith('/upload', expect.any(FormData));
    expect(result.message).toBe('Uploaded');
  });

  it('transcribeAudio should send a POST request with path and language', async () => {
    axios.post.mockResolvedValue({ data: { text: 'Hello' } });
    
    const result = await apiService.transcribeAudio('/path/to/file', 'zh');
    
    expect(axios.post).toHaveBeenCalledWith('/transcribe', {
      file_path: '/path/to/file',
      language: 'zh',
    });
    expect(result.text).toBe('Hello');
  });

  it('generateContent should send a POST request with transcript and type', async () => {
    axios.post.mockResolvedValue({ data: { content: 'Summary' } });
    
    const result = await apiService.generateContent('Raw text', 'summary');
    
    expect(axios.post).toHaveBeenCalledWith('/generate', {
      transcript: 'Raw text',
      template_type: 'summary',
    });
    expect(result.content).toBe('Summary');
  });
});
