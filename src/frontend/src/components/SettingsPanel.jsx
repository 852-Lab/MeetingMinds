import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const SettingsPanel = ({ onKeyStatusChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [keyConfigured, setKeyConfigured] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    apiService.getOpenAIKeyStatus()
      .then(({ configured }) => {
        setKeyConfigured(configured);
        onKeyStatusChange?.(configured);
      })
      .catch(() => {});
  }, []);

  const handleSave = async () => {
    if (!apiKey.trim()) return;
    setSaving(true);
    setMessage(null);
    try {
      await apiService.saveOpenAIKey(apiKey.trim());
      setKeyConfigured(true);
      setApiKey('');
      setMessage({ type: 'success', text: 'OpenAI key saved. All jobs will now use Whisper via the API.' });
      onKeyStatusChange?.(true);
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to save key.' });
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    setSaving(true);
    setMessage(null);
    try {
      await apiService.deleteOpenAIKey();
      setKeyConfigured(false);
      setApiKey('');
      setMessage({ type: 'success', text: 'Key removed. Jobs will use the local transcription engine.' });
      onKeyStatusChange?.(false);
    } catch {
      setMessage({ type: 'error', text: 'Failed to remove key.' });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="bg-white/40 backdrop-blur-lg border border-white/40 rounded-3xl shadow-xl overflow-hidden">
      <button
        onClick={() => setIsOpen(o => !o)}
        className="w-full flex items-center justify-between p-6 text-left hover:bg-white/20 transition-colors"
      >
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-emerald-100 rounded-2xl text-emerald-600">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <div>
            <h2 className="text-lg font-bold text-gray-800">Transcription Settings</h2>
            <p className="text-sm text-gray-500 font-medium">
              {keyConfigured
                ? 'Using OpenAI Whisper API'
                : 'Using local Whisper engine'}
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <span className={`inline-flex items-center space-x-1.5 px-3 py-1 rounded-full text-xs font-bold ${
            keyConfigured
              ? 'bg-emerald-100 text-emerald-700'
              : 'bg-gray-100 text-gray-500'
          }`}>
            <span className={`w-1.5 h-1.5 rounded-full ${keyConfigured ? 'bg-emerald-500' : 'bg-gray-400'}`} />
            <span>{keyConfigured ? 'OpenAI Active' : 'Local'}</span>
          </span>
          <svg
            className={`w-5 h-5 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </button>

      {isOpen && (
        <div className="px-6 pb-6 border-t border-gray-100/50">
          <div className="pt-6 space-y-4">
            <div>
              <p className="text-sm text-gray-600 mb-4">
                Enter your <span className="font-semibold text-gray-800">OpenAI API key</span> to route all
                transcription jobs through the Whisper API instead of the local engine. The key is encrypted
                before being stored.
              </p>

              {keyConfigured && (
                <div className="flex items-center space-x-3 p-3 bg-emerald-50 border border-emerald-200 rounded-2xl mb-4">
                  <svg className="w-4 h-4 text-emerald-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                  <p className="text-sm text-emerald-700 font-medium">API key is configured and active</p>
                </div>
              )}

              <div className="flex space-x-3">
                <input
                  type="password"
                  value={apiKey}
                  onChange={e => setApiKey(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && handleSave()}
                  placeholder={keyConfigured ? 'Enter new key to replace existing...' : 'sk-...'}
                  className="flex-1 p-3 bg-white/70 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all placeholder:text-gray-400 text-sm font-mono"
                />
                <button
                  onClick={handleSave}
                  disabled={!apiKey.trim() || saving}
                  className="px-5 py-3 bg-emerald-600 text-white rounded-2xl font-bold text-sm hover:bg-emerald-700 disabled:opacity-50 transition-all shadow-lg shadow-emerald-100 active:scale-95"
                >
                  {saving ? 'Saving...' : 'Save'}
                </button>
                {keyConfigured && (
                  <button
                    onClick={handleDelete}
                    disabled={saving}
                    className="px-5 py-3 bg-red-50 text-red-600 border border-red-200 rounded-2xl font-bold text-sm hover:bg-red-100 disabled:opacity-50 transition-all active:scale-95"
                  >
                    Remove
                  </button>
                )}
              </div>
            </div>

            {message && (
              <p className={`text-sm font-medium ${message.type === 'success' ? 'text-emerald-600' : 'text-red-600'}`}>
                {message.text}
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SettingsPanel;
