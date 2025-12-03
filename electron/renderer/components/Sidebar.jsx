import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = () => {
  const location = useLocation();

  const navItems = [
    { path: '/dashboard', icon: '📊', label: 'Dashboard' },
    { path: '/downloads', icon: '⬇️', label: 'Downloads' },
    { path: '/parser', icon: '⚙️', label: 'Parser' },
    { path: '/settings', icon: '⚙️', label: 'Settings' },
    { path: '/logs', icon: '📋', label: 'Logs' },
  ];

  return (
    <aside className="w-48 bg-sidebar-bg text-white flex flex-col shadow-lg">
      <div className="p-5 border-b border-gray-600">
        <h1 className="text-xl font-semibold">HomeStock</h1>
      </div>
      <nav className="flex-1 py-2">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-5 py-3 text-sm transition-colors ${
                isActive
                  ? 'bg-primary-500 text-white'
                  : 'text-gray-200 hover:bg-sidebar-hover'
              }`}
            >
              <span className="text-lg">{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
};

export default Sidebar;

