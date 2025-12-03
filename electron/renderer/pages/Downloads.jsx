import React, { useState, useEffect } from 'react';
import { downloadsAPI, settingsAPI } from '../services/api';
import FormInput from '../components/FormInput';
import Button from '../components/Button';
import StatusMessage from '../components/StatusMessage';

const Downloads = () => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [urls, setUrls] = useState({
    fo_udiff: '',
    fo_participant_oi: '',
    cm_delivery: '',
    cm_udiff: '',
    cm_bhavcopy: '',
  });
  const [downloads, setDownloads] = useState([]);
  const [status, setStatus] = useState({ message: '', type: '' });
  const [pollingInterval, setPollingInterval] = useState(null);

  useEffect(() => {
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    setStartDate(yesterday.toISOString().split('T')[0]);
    setEndDate(today.toISOString().split('T')[0]);
    
    loadDownloadStatus(yesterday.toISOString().split('T')[0], today.toISOString().split('T')[0]);
    
    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
    };
  }, []);

  const loadDownloadStatus = async (start, end) => {
    try {
      const data = await downloadsAPI.getStatus(start, end);
      if (data.success) {
        setDownloads(data.downloads || []);
      }
    } catch (error) {
      console.error('Error loading download status:', error);
    }
  };

  const startPolling = (start, end) => {
    if (pollingInterval) {
      clearInterval(pollingInterval);
    }

    const interval = setInterval(async () => {
      await loadDownloadStatus(start, end);
      
      const data = await downloadsAPI.getStatus(start, end);
      if (data.success) {
        const activeDownloads = data.downloads.filter(
          (d) => d.status === 'pending' || d.status === 'downloading'
        );
        
        if (activeDownloads.length === 0) {
          clearInterval(interval);
          setPollingInterval(null);
          setStatus({ message: 'All downloads completed!', type: 'success' });
          setTimeout(() => setStatus({ message: '', type: '' }), 5000);
        }
      }
    }, 2000);

    setPollingInterval(interval);
  };

  const handleDownloadMissing = async () => {
    try {
      setStatus({ message: 'Starting downloads...', type: 'info' });
      
      const settingsData = await settingsAPI.getSettings();
      const rawPath = settingsData.success ? settingsData.settings?.raw_path || '' : '';
      
      await downloadsAPI.downloadMissing(startDate, endDate, urls, rawPath);
      startPolling(startDate, endDate);
      await loadDownloadStatus(startDate, endDate);
    } catch (error) {
      setStatus({ message: `Error: ${error.message}`, type: 'error' });
    }
  };

  const handleRefresh = async () => {
    await loadDownloadStatus(startDate, endDate);
  };

  const handleRetry = async (downloadId) => {
    try {
      setStatus({ message: 'Retrying download...', type: 'info' });
      const data = await downloadsAPI.retryDownload(downloadId);
      
      if (data.success) {
        setTimeout(async () => {
          await loadDownloadStatus(startDate, endDate);
        }, 1000);
      } else {
        setStatus({ message: `Retry failed: ${data.error}`, type: 'error' });
      }
    } catch (error) {
      setStatus({ message: `Error: ${error.message}`, type: 'error' });
    }
  };

  const handleUrlChange = (key, value) => {
    setUrls((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div>
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">Downloads</h2>

      <div className="bg-white p-5 rounded-lg shadow-sm mb-5">
        <div className="grid grid-cols-2 gap-4 mb-5">
          <FormInput
            label="Start Date"
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
          <FormInput
            label="End Date"
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </div>

        <h3 className="text-lg font-semibold text-gray-800 mb-4">URLs</h3>
        <FormInput
          label="F&O UDiFF URL"
          value={urls.fo_udiff}
          onChange={(e) => handleUrlChange('fo_udiff', e.target.value)}
          placeholder="https://..."
        />
        <FormInput
          label="F&O Participant OI URL"
          value={urls.fo_participant_oi}
          onChange={(e) => handleUrlChange('fo_participant_oi', e.target.value)}
          placeholder="https://..."
        />
        <FormInput
          label="CM Delivery URL"
          value={urls.cm_delivery}
          onChange={(e) => handleUrlChange('cm_delivery', e.target.value)}
          placeholder="https://..."
        />
        <FormInput
          label="CM UDiFF URL"
          value={urls.cm_udiff}
          onChange={(e) => handleUrlChange('cm_udiff', e.target.value)}
          placeholder="https://..."
        />
        <FormInput
          label="CM Bhavcopy URL"
          value={urls.cm_bhavcopy}
          onChange={(e) => handleUrlChange('cm_bhavcopy', e.target.value)}
          placeholder="https://..."
        />
      </div>

      <div className="flex gap-4 mb-5">
        <Button onClick={handleDownloadMissing}>Download Missing Files</Button>
        <Button variant="secondary" onClick={handleRefresh}>
          Refresh Status
        </Button>
      </div>

      <StatusMessage message={status.message} type={status.type} />

      <div className="bg-white p-5 rounded-lg shadow-sm mt-5">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Download Status</h3>
        <div className="space-y-4">
          {downloads.length === 0 ? (
            <p className="text-gray-500 text-center py-5">No downloads found</p>
          ) : (
            downloads.map((download) => (
              <div
                key={download.id}
                className={`p-4 border rounded-lg ${
                  download.status === 'completed'
                    ? 'border-green-500 bg-green-50'
                    : download.status === 'failed'
                    ? 'border-red-500 bg-red-50'
                    : download.status === 'downloading'
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-300 bg-gray-50'
                }`}
              >
                <div className="flex justify-between items-center mb-2">
                  <span className="font-semibold text-sm text-gray-800">
                    {download.file_name}
                  </span>
                  <span
                    className={`text-xs px-2 py-1 rounded ${
                      download.status === 'completed'
                        ? 'bg-green-200 text-green-800'
                        : download.status === 'failed'
                        ? 'bg-red-200 text-red-800'
                        : download.status === 'downloading'
                        ? 'bg-blue-200 text-blue-800'
                        : 'bg-gray-200 text-gray-800'
                    }`}
                  >
                    {download.status.toUpperCase()}
                  </span>
                </div>
                <div className="mb-2">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all ${
                        download.status === 'completed'
                          ? 'bg-green-500'
                          : 'bg-blue-500'
                      }`}
                      style={{ width: `${download.progress || 0}%` }}
                    />
                  </div>
                  <div className="text-xs text-gray-600 mt-1">
                    {Math.round(download.progress || 0)}%
                  </div>
                </div>
                <div className="flex justify-between items-center text-xs text-gray-600">
                  <span>
                    Date: {download.date_str} | Type: {download.file_type}
                  </span>
                  <div className="flex gap-2">
                    {download.status === 'failed' && (
                      <button
                        onClick={() => handleRetry(download.id)}
                        className="px-3 py-1 bg-orange-500 text-white rounded text-xs hover:bg-orange-600"
                      >
                        🔄 Retry
                      </button>
                    )}
                    {download.error_message && (
                      <span className="text-red-600 text-xs">
                        {download.error_message}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Downloads;

