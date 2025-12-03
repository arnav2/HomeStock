import React, { useState, useEffect } from 'react';
import { dashboardAPI, settingsAPI } from '../services/api';
import StatusCard from '../components/StatusCard';
import Button from '../components/Button';
import StatusMessage from '../components/StatusMessage';

const Dashboard = () => {
  const [filesDownloaded, setFilesDownloaded] = useState('-');
  const [filesMissing, setFilesMissing] = useState('-');
  const [lastRun, setLastRun] = useState('Never');
  const [status, setStatus] = useState({ message: '', type: '' });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const today = new Date().toISOString().split('T')[0];
      const data = await dashboardAPI.getStatus(today);
      setFilesDownloaded(data.downloaded?.length || 0);
      setFilesMissing(data.missing?.length || 0);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    }
  };

  const handleRunFullAutomation = async () => {
    setLoading(true);
    setStatus({ message: 'Running full automation...', type: 'info' });
    
    try {
      const data = await dashboardAPI.runFullAutomation();
      
      if (data.success) {
        setStatus({ message: 'Automation completed successfully!', type: 'success' });
        loadDashboard();
        setTimeout(() => setStatus({ message: '', type: '' }), 5000);
      } else {
        setStatus({ message: `Error: ${data.error}`, type: 'error' });
      }
    } catch (error) {
      setStatus({ message: `Error: ${error.message}`, type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleOpenOutputFolder = async () => {
    try {
      const settingsData = await settingsAPI.getSettings();
      if (settingsData.success && settingsData.settings?.output_path) {
        await window.electronAPI.openFolder(settingsData.settings.output_path);
      } else {
        alert('Please set output folder in Settings first');
      }
    } catch (error) {
      alert('Error opening folder: ' + error.message);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">Dashboard</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
        <StatusCard title="Files Downloaded" value={filesDownloaded} />
        <StatusCard title="Files Missing" value={filesMissing} />
        <StatusCard title="Last Run" value={lastRun} />
      </div>

      <div className="flex gap-4 mb-6">
        <Button 
          onClick={handleRunFullAutomation} 
          disabled={loading}
        >
          {loading ? 'Running...' : 'Run Full Automation Now'}
        </Button>
        <Button variant="secondary" onClick={handleOpenOutputFolder}>
          Open Output Folder
        </Button>
      </div>

      <StatusMessage message={status.message} type={status.type} />
    </div>
  );
};

export default Dashboard;

