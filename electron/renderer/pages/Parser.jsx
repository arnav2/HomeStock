import React, { useState, useEffect } from 'react';
import { parserAPI, settingsAPI } from '../services/api';
import FormInput from '../components/FormInput';
import Button from '../components/Button';
import StatusMessage from '../components/StatusMessage';

const Parser = () => {
  const [rawPath, setRawPath] = useState('');
  const [outputPath, setOutputPath] = useState('');
  const [status, setStatus] = useState({ message: '', type: '' });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const data = await settingsAPI.getSettings();
      if (data.success && data.settings) {
        setRawPath(data.settings.raw_path || '');
        setOutputPath(data.settings.output_path || '');
      }
    } catch (error) {
      console.error('Error loading settings:', error);
    }
  };

  const handleSelectRawPath = async () => {
    try {
      const folder = await window.electronAPI.selectFolder();
      if (folder) {
        setRawPath(folder);
      }
    } catch (error) {
      console.error('Error selecting folder:', error);
    }
  };

  const handleSelectOutputPath = async () => {
    try {
      const folder = await window.electronAPI.selectFolder();
      if (folder) {
        setOutputPath(folder);
      }
    } catch (error) {
      console.error('Error selecting folder:', error);
    }
  };

  const handleParseFiles = async () => {
    if (!rawPath || !outputPath) {
      setStatus({ message: 'Please select both raw and output paths', type: 'error' });
      return;
    }

    setLoading(true);
    setStatus({ message: 'Parsing files...', type: 'info' });
    setResults(null);

    try {
      const data = await parserAPI.parseFiles(rawPath, outputPath);
      
      if (data.success) {
        setStatus({ message: 'Parsing completed!', type: 'success' });
        setResults(data.results || {});
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

  return (
    <div>
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">Parser</h2>

      <div className="bg-white p-5 rounded-lg shadow-sm mb-5">
        <div className="flex items-end gap-2 mb-4">
          <div className="flex-1">
            <FormInput
              label="Raw Files Path"
              value={rawPath}
              onChange={(e) => setRawPath(e.target.value)}
              readonly
            />
          </div>
          <Button small onClick={handleSelectRawPath}>
            Browse
          </Button>
        </div>

        <div className="flex items-end gap-2">
          <div className="flex-1">
            <FormInput
              label="Output Path"
              value={outputPath}
              onChange={(e) => setOutputPath(e.target.value)}
              readonly
            />
          </div>
          <Button small onClick={handleSelectOutputPath}>
            Browse
          </Button>
        </div>
      </div>

      <Button onClick={handleParseFiles} disabled={loading}>
        {loading ? 'Parsing...' : 'Parse Raw Files → Normalized CSV'}
      </Button>

      <StatusMessage message={status.message} type={status.type} />

      {results && Object.keys(results).length > 0 && (
        <div className="bg-white p-5 rounded-lg shadow-sm mt-5">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Parse Results</h3>
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-4 py-2 text-left border-b border-gray-200 font-semibold text-gray-800">
                  Table
                </th>
                <th className="px-4 py-2 text-left border-b border-gray-200 font-semibold text-gray-800">
                  Row Count
                </th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(results).map(([tableName, count]) => (
                <tr key={tableName} className="border-b border-gray-200">
                  <td className="px-4 py-2">{tableName}</td>
                  <td className="px-4 py-2">{count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Parser;

