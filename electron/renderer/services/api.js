import axios from 'axios';

const BACKEND_URL = 'http://localhost:5001';

const api = axios.create({
  baseURL: BACKEND_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Dashboard API
export const dashboardAPI = {
  getStatus: async (date) => {
    const response = await api.post('/download/', {
      start_date: date,
      end_date: date,
      urls: {},
      raw_path: '',
    });
    return response.data;
  },
  runFullAutomation: async () => {
    const response = await api.post('/run-full/');
    return response.data;
  },
};

// Downloads API
export const downloadsAPI = {
  getStatus: async (startDate, endDate) => {
    const response = await api.get(`/download/status?start_date=${startDate}&end_date=${endDate}`);
    return response.data;
  },
  downloadMissing: async (startDate, endDate, urls, rawPath) => {
    const fileTypes = ['fo_udiff', 'fo_participant_oi', 'cm_delivery', 'cm_udiff', 'cm_bhavcopy', 'fo_bhavcopy'];
    const downloadPromises = [];
    
    const start = new Date(startDate);
    const end = new Date(endDate);
    const current = new Date(start);
    
    while (current <= end) {
      const dateStr = current.toISOString().split('T')[0];
      for (const fileType of fileTypes) {
        const url = urls[fileType] || '';
        downloadPromises.push(
          api.post('/download/single', {
            file_type: fileType,
            date_str: dateStr,
            url: url,
            raw_path: rawPath,
            custom_urls: urls,
          })
        );
      }
      current.setDate(current.getDate() + 1);
    }
    
    return Promise.allSettled(downloadPromises);
  },
  retryDownload: async (downloadId) => {
    const response = await api.post('/download/retry', {
      download_id: downloadId,
    });
    return response.data;
  },
};

// Parser API
export const parserAPI = {
  parseFiles: async (rawPath, outputPath) => {
    const response = await api.post('/parse/', {
      raw_path: rawPath,
      output_path: outputPath,
    });
    return response.data;
  },
};

// Settings API
export const settingsAPI = {
  getSettings: async () => {
    const response = await api.get('/settings/get');
    return response.data;
  },
  saveSettings: async (settings) => {
    const response = await api.post('/settings/save', settings);
    return response.data;
  },
  testPath: async (path) => {
    const response = await api.post('/settings/test-path', { path });
    return response.data;
  },
};

// Logs API
export const logsAPI = {
  getLogs: async () => {
    const response = await api.get('/logs');
    return response.data;
  },
};

export default api;

