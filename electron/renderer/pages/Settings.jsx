import React, { useState, useEffect } from 'react';
import { settingsAPI } from '../services/api';
import FormInput from '../components/FormInput';
import Button from '../components/Button';
import StatusMessage from '../components/StatusMessage';

const Settings = () => {
  const [settings, setSettings] = useState({
    raw_path: '',
    processed_path: '',
    output_path: '',
    scheduler: 'off',
    custom_cron: '',
  });
  const [status, setStatus] = useState({ message: '', type: '' });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const data = await settingsAPI.getSettings();
      if (data.success && data.settings) {
        setSettings({
          raw_path: data.settings.raw_path || '',
          processed_path: data.settings.processed_path || '',
          output_path: data.settings.output_path || '',
          scheduler: data.settings.scheduler || 'off',
          custom_cron: data.settings.custom_cron || '',
        });
      }
    } catch (error) {
      console.error('Error loading settings:', error);
    }
  };

  const handleSelectFolder = async (field) => {
    try {
      const folder = await window.electronAPI.selectFolder();
      if (folder) {
        setSettings((prev) => ({ ...prev, [field]: folder }));
      }
    } catch (error) {
      console.error('Error selecting folder:', error);
    }
  };

  const handleSaveSettings = async () => {
    setLoading(true);
    try {
      const data = await settingsAPI.saveSettings(settings);
      
      if (data.success) {
        setStatus({ message: 'Settings saved successfully!', type: 'success' });
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

  const handleTestFolders = async () => {
    const results = [];
    
    for (const [key, path] of Object.entries(settings)) {
      if (key.includes('_path') && path) {
        try {
          const data = await settingsAPI.testPath(path);
          results.push(
            `${key}: ${data.accessible ? '✓ Accessible' : '✗ Not accessible'}`
          );
        } catch (error) {
          results.push(`${key}: ✗ Error testing`);
        }
      }
    }
    
    setStatus({ message: results.join('<br>'), type: 'info' });
  };

  return (
    <div>
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">Settings</h2>

      <div className="bg-white p-5 rounded-lg shadow-sm mb-5">
        <div className="flex items-end gap-2 mb-4">
          <div className="flex-1">
            <FormInput
              label="Default Raw File Folder"
              value={settings.raw_path}
              onChange={(e) =>
                setSettings((prev) => ({ ...prev, raw_path: e.target.value }))
              }
              readonly
            />
          </div>
          <Button small onClick={() => handleSelectFolder('raw_path')}>
            Browse
          </Button>
        </div>

        <div className="flex items-end gap-2 mb-4">
          <div className="flex-1">
            <FormInput
              label="Default Processed Folder"
              value={settings.processed_path}
              onChange={(e) =>
                setSettings((prev) => ({ ...prev, processed_path: e.target.value }))
              }
              readonly
            />
          </div>
          <Button small onClick={() => handleSelectFolder('processed_path')}>
            Browse
          </Button>
        </div>

        <div className="flex items-end gap-2">
          <div className="flex-1">
            <FormInput
              label="Default Output Folder"
              value={settings.output_path}
              onChange={(e) =>
                setSettings((prev) => ({ ...prev, output_path: e.target.value }))
              }
              readonly
            />
          </div>
          <Button small onClick={() => handleSelectFolder('output_path')}>
            Browse
          </Button>
        </div>
      </div>

      <div className="bg-white p-5 rounded-lg shadow-sm mb-5">
        <div className="mb-4">
          <label className="block mb-1.5 text-sm font-medium text-gray-700">
            Scheduler
          </label>
          <select
            value={settings.scheduler}
            onChange={(e) =>
              setSettings((prev) => ({ ...prev, scheduler: e.target.value }))
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="off">Off</option>
            <option value="daily-7am">Daily at 7 AM</option>
            <option value="custom">Custom Cron</option>
          </select>
        </div>

        {settings.scheduler === 'custom' && (
          <FormInput
            label="Custom Cron String"
            value={settings.custom_cron}
            onChange={(e) =>
              setSettings((prev) => ({ ...prev, custom_cron: e.target.value }))
            }
            placeholder="0 7 * * *"
          />
        )}
      </div>

      <div className="flex gap-4 mb-5">
        <Button onClick={handleSaveSettings} disabled={loading}>
          {loading ? 'Saving...' : 'Save Settings'}
        </Button>
        <Button variant="secondary" onClick={handleTestFolders}>
          Test Folder Accessibility
        </Button>
      </div>

      <StatusMessage message={status.message} type={status.type} />
    </div>
  );
};

export default Settings;

