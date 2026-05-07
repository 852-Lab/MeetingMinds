import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import MediaInput from '../components/MediaInput';
import React from 'react';

describe('MediaInput', () => {
  it('should call onYouTube when YouTube button is clicked', () => {
    const onYouTube = vi.fn();
    render(<MediaInput onUpload={() => {}} onYouTube={onYouTube} loading={false} />);
    
    const input = screen.getByPlaceholderText(/Paste YouTube link/i);
    fireEvent.change(input, { target: { value: 'https://youtube.com/test' } });
    
    const button = screen.getByText(/Extract Transcript/i);
    fireEvent.click(button);
    
    expect(onYouTube).toHaveBeenCalledWith('https://youtube.com/test');
  });

  it('should disable buttons when loading', () => {
    render(<MediaInput onUpload={() => {}} onYouTube={() => {}} loading={true} />);
    
    const uploadButton = screen.getByText(/Process File/i);
    const ytButton = screen.getByText(/Extract Transcript/i);
    
    expect(uploadButton).toBeDisabled();
    expect(ytButton).toBeDisabled();
  });
});
