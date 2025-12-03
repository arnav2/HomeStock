import React, { useEffect, useState } from 'react';
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Downloads from './pages/Downloads';
import Parser from './pages/Parser';
import Settings from './pages/Settings';
import Logs from './pages/Logs';

function App() {
  const [backendReady, setBackendReady] = useState(false);
  const [backendError, setBackendError] = useState(null);

  useEffect(() => {
    // Listen for backend ready event
    if (window.electronAPI) {
      window.electronAPI.onBackendReady(() => {
        console.log('Backend is ready');
        setBackendReady(true);
      });

      window.electronAPI.onBackendError((event, error) => {
        console.error('Backend error:', error);
        setBackendError(error);
      });
    }
  }, []);

  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-8">
          {backendError && (
            <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
              Backend Error: {backendError}
            </div>
          )}
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/downloads" element={<Downloads />} />
            <Route path="/parser" element={<Parser />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/logs" element={<Logs />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

