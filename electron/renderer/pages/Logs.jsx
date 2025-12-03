import React, { useState, useEffect } from 'react';
import { logsAPI, settingsAPI } from '../services/api';
import Button from '../components/Button';

const Logs = () => {
  const [logs, setLogs] = useState('Loading logs...');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadLogs();
  }, []);

  const loadLogs = async () => {
    setLoading(true);
    try {
      const data = await logsAPI.getLogs();
      
      if (data.success) {
        setLogs(data.logs || 'No logs available');
      } else {
        setLogs(`Error: ${data.error}`);
      }
    } catch (error) {
      setLogs(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenLogFile = async () => {
    try {
      const settingsData = await settingsAPI.getSettings();
      if (settingsData.success && settingsData.settings?.log_path) {
        await window.electronAPI.openFolder(settingsData.settings.log_path);
      }
    } catch (error) {
      console.error('Error opening log file:', error);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">Logs</h2>

      <div className="flex gap-4 mb-5">
        <Button onClick={loadLogs} disabled={loading}>
          {loading ? 'Loading...' : 'Refresh'}
        </Button>
        <Button variant="secondary" onClick={handleOpenLogFile}>
          Open Full Log File
        </Button>
      </div>

      <div className="bg-gray-900 text-gray-100 p-5 rounded-lg mt-5 max-h-[500px] overflow-y-auto font-mono text-xs">
        <pre className="whitespace-pre-wrap break-words">{logs}</pre>
      </div>
    </div>
  );
};

export default Logs;

