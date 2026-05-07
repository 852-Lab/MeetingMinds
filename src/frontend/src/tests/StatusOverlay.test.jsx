import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import StatusOverlay from '../components/StatusOverlay';
import React from 'react';

describe('StatusOverlay', () => {
  it('should not render when no status and not loading', () => {
    const { container } = render(<StatusOverlay status="" progress={0} loading={false} />);
    expect(container.firstChild).toBeNull();
  });

  it('should render status message', () => {
    render(<StatusOverlay status="Processing..." progress={0} loading={false} />);
    expect(screen.getByText('Processing...')).toBeInTheDocument();
  });

  it('should show progress bar when loading and progress > 0', () => {
    const { container } = render(<StatusOverlay status="Loading..." progress={50} loading={true} />);
    const progressBar = container.querySelector('.bg-gradient-to-r');
    expect(progressBar).toBeInTheDocument();
    expect(progressBar.style.width).toBe('50%');
  });

  it('should show loading dots when loading', () => {
    const { container } = render(<StatusOverlay status="Loading..." progress={0} loading={true} />);
    const dots = container.querySelectorAll('.animate-bounce');
    expect(dots.length).toBe(3);
  });
});
